from apps.user.models import User
from uuid import uuid4
from utils import cache, mail
from django.http import response
from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


class RegisterView(generic.CreateView):
    template_name = "auth/sign_up.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone_number = request.POST.get("phone_number", None)
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        email = request.POST.get("email", None)
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        password_1 = request.POST.get("password_1", None)
        if not all(
            (username, password, email, first_name, last_name, username, password_1)
        ):
            return response.HttpResponse(
                " This field' should not be null !", status=400
            )
        if not password_1 == password:
            return response.HttpResponse(
                request, "password and confirm is not simillar."
            )
        else:
            user, created = User.objects.get_or_create(
                phone_number=phone_number,
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save()
            if not created:
                return response.HttpResponse("User already registered!", status=400)
            # activate
            if not cache.get_or_create(
                f"activate_token_user_{user.username}", lambda: uuid4().hex, 180
            ):
                # send mail !
                mail.send_mail(
                    f"Verification {user.username}",
                    user.email,
                    "auth/verify.html",
                    {
                        "user": user,
                        "token": cache.cache.get(
                            f"activate_token_user_{user.username}"
                        ),
                        "host": self.request.get_host(),
                    },
                )

                return redirect("send_email")


            class LoginView(generic.View):
                template_name = "auth/sign_in.html"

                def get(self, request):
                    return render(request, self.template_name)

                def post(self, request):
                    username = self.request.POST.get("username", None)
                    password = self.request.POST.get("password", None)

                    if not all((username, password)):
                        return response.HttpResponse(
                            "'username' or 'password' should not be null !", status=400
                        )

                    if user := authenticate(password=password, username=username):
                        if user.is_active:
                            login(self.request, user)
                            return redirect("home")

                        # activate
                        if not cache.get_or_create(
                                f"activate_token_user_{user.username}", lambda: uuid4().hex, 300
                        ):
                            # send mail !
                            mail.send_mail(
                                f"Verification {user.username}",
                                user.email,
                                "mail/verify.html",
                                {
                                    "user": user,
                                    "token": cache.cache.get(
                                        f"activate_token_user_{user.username}"
                                    ),
                                    "host": self.request.get_host(),
                                },
                            )
                            return redirect("send_email")
                    return response.HttpResponse("User not found !", status=404)
