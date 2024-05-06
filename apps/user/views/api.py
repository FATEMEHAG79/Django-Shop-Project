from apps.user.models import User
from uuid import uuid4
from django.http import response
from utils import cache, mail
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


class SendOtp(generic.CreateView):
    template_name = "auth/sendotp.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email", None)
        if not email:
            messages.info(request, "email should not be Null.")
            return redirect("signup/in")
        # otp
        token = uuid4().hex
        if not cache.get_or_create(email, token, 120):
            code = "".join([car for car in token if car.isnumeric()][0:4])
            # send mail !
            mail.send_mail(
                f"Verification {email}",
                email,
                "auth/email-otp.html",
                {"user": email, "code": code},
            )
            user = User.objects.filter(email=email).exists()
            if user:
                return redirect("confirmotp", email, token)
            else:
                return redirect("confirmotpregister", email, token)
        messages.info(request, "otp send !please try after 3 minitue.")
        return redirect("signup/in")


class ConfirmOtp(generic.View):
    template_name = "auth/sign_in.html"

    def get(self, request, email, token):
        context = {"email": email, "token": token}
        return render(request, self.template_name, context)

    def post(self, request, token, email):
        otp = self.request.POST.get("otp", None)
        if not otp:
            return response.HttpResponse("otp should not be null !", status=400)
        code = "".join([car for car in token if car.isnumeric()][0:4])
        if otp == code:
            user = User.objects.get(email=email)
            if user := authenticate(password=user.password, username=user.username):
                if user.is_active:
                    login(self.request, user)
                    return redirect("home")
                # activate
                if not cache.get_or_create(
                    f"activate_token_user_{user.username}", lambda: uuid4().hex, 120
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
                messages.info(
                    request, "email verification send !please try after 2 minitue."
                )
                return redirect("send_email")
        else:
            messages.info(request, "otp is not correct.")
            return redirect("confirmotp", email, token)


class LoginView(generic.View):
    template_name = "auth/sign_in.html"

    def get(self, request, email, token):
        context = {"email": email, "token": token}
        return render(request, self.template_name, context)

    def post(self, request, email, token):
        username = self.request.POST.get("username", None)
        password = self.request.POST.get("password", None)

        if not all((username, password)):
            messages.info(request, "'username' or 'password' should not be null !")
            return redirect("home")

        if user := authenticate(password=password, username=username):
            if user.is_active:
                login(self.request, user)
                return redirect("home")

            # activate
            if not cache.get_or_create(
                f"activate_token_user_{user.username}", lambda: uuid4().hex, 120
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
            messages.info("otp send !please try after 3 minitue.")
            return redirect("login")


class ConfirmOtpRegister(generic.View):
    template_name = "auth/confirmotp_signup.html"

    def get(self, request, email, token):
        context = {"email": email, "token": token}
        return render(request, self.template_name, context)

    def post(self, request, email, token):
        otp = self.request.POST.get("otp", None)
        if not otp:
            messages.info(request, "otp should not be Null.")
            return redirect("confirmotpregister", email, token)
        token_ = cache.cache.get(email)
        code = "".join([car for car in token if car.isnumeric()][0:4])
        if otp == code:
            user = User.objects.create_user(self, email=email)
            user.save()
            return redirect("register", email)
        messages.info(request, "otp is not correct.")
        return redirect("register", email, token)


class Registeration(generic.View):
    template_name = "auth/register.html"

    def get(self, request, email):
        context = {"email": email}
        return render(request, self.template_name, context)

    def post(self, request, email):
        username = self.request.POST.get("username", None)
        password = self.request.POST.get("password", None)
        confirmpassword = self.request.POST.get("password1", None)
        if not all((username, password, confirmpassword)):
            messages.info(request, "this field should not be Null.")
            return redirect("register", email)
        if password == confirmpassword:
            user = User.objects.get(email=email)
            user.username = username
            user.set_password(password)
            user.save()
            # activate
            if not cache.get_or_create(
                f"activate_token_user_{user.username}", lambda: uuid4().hex, 120
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
        messages.info(request, "password and confirm password is not match.")
        return redirect("register", email)
