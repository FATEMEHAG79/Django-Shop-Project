from apps.user.models import User
from uuid import uuid4
from django.http import response, HttpResponse
from utils import cache, mail
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


class SendOtp(generic.CreateView):
    template_name = "auth/sendotp.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", None)
        # otp
        token = uuid4().hex
        code = "".join([car for car in token if car.isnumeric()][0:4])
        if not cache.get_or_create(email, code, 120):
            # send mail !
            mail.send_mail(
                f"Verification {email}",
                email,
                "auth/email-otp.html",
                {"user": email, "code": code},
            )
            user = User.objects.filter(email=email).exists()
            if user:
                return redirect(f"confirmotp/?email={email}")
            else:
                return redirect(f"confirmregistration/?email={email}")
        success = "otp send !please try after 3 minitue."
        return HttpResponse(success)


class ConfirmOtp(generic.View):
    template_name = "auth/sign_in.html"

    def get(self, request):
        email = request.GET.get("email")
        return render(request, self.template_name, {"email": email})

    def post(self, request):
        otp = self.request.POST.get("otp", None)
        email = self.request.POST.get("email")
        if not otp:
            return response.HttpResponse("otp should not be null !", status=400)
        code = cache.cache.get(email)
        if otp == code:
            user = User.objects.get(email=email)
            if user.DoesNotExist:
                if user.is_active:
                    cache.cache.delete(email)
                    login(self.request, user)
                    return redirect("home")
                # activate
                if not cache.get_or_create(
                    f"activate_token_user_{user.username}", lambda: uuid4().hex, 120
                ):
                    cache.cache.delete(email)
                    login(self.request, user)
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
                return HttpResponse(
                    "email verification send !please try after 2 minitue."
                )
        else:
            return HttpResponse("otp is not correct.")


class LoginView(generic.View):
    template_name = "auth/sign_in.html"

    def get(self, request):
        email = request.GET.get("email")
        return render(request, self.template_name, {"email": email})

    def post(self, request):
        email = self.request.POST.get("email")
        username = self.request.POST.get("username", None)
        password = self.request.POST.get("password", None)

        if user := authenticate(password=password, username=username):
            if user.is_active:
                cache.cache.delete(email)
                login(self.request, user)
                return redirect("home")
            # activate
            if not cache.get_or_create(
                f"activate_token_user_{user.username}", lambda: uuid4().hex, 120
            ):
                cache.cache.delete(email)
                login(self.request, user)
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
            return HttpResponse("otp send !please try after 3 minitue.")
        return HttpResponse("username or password is not correct.please try again")


class ConfirmOtpRegister(generic.View):
    template_name = "auth/confirmotp_signup.html"

    def get(self, request):
        email = request.GET.get("email")
        return render(request, self.template_name, {"email": email})

    def post(self, request):
        email = self.request.POST.get("email")
        otp = self.request.POST.get("otp", None)
        if not otp:
            messages.info(request, "otp should not be Null.")
            return redirect(f"confirmregistration/?email={email}")

        code = cache.cache.get(email)
        if otp == code:
            user = User.objects.create_user(self, email=email)
            user.save()
            return redirect("register", email)
        return HttpResponse("otp is not correct.")


class Registeration(generic.View):
    template_name = "auth/register.html"

    def get(self, request, email):
        return render(request, self.template_name, {"email": email})

    def post(self, request, email):
        username = self.request.POST.get("username", None)
        phone_number = self.request.POST.get("phone_number", None)
        password = self.request.POST.get("password", None)
        confirmpassword = self.request.POST.get("password1", None)
        if password == confirmpassword:
            user = User.objects.get(email=email)
            user.username = username
            user.phone_number = phone_number
            user.set_password(password)
            user.save()
            # activate
            if not cache.get_or_create(
                f"activate_token_user_{user.username}", lambda: uuid4().hex, 120
            ):
                cache.cache.delete(email)
                login(self.request, user)
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
        return HttpResponse("password and confirm password is not match.")
