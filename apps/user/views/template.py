from uuid import uuid4
from apps.order.models import Order
from apps.user.models import Address
from utils import cache
from django.http import response
from django.views import generic, View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from utils import mail
from django.shortcuts import redirect
from django.http import HttpResponse

User = get_user_model()


class VerificationView(generic.View):
    template_name = "auth/verify_successful.html"

    def get(self, request, username, token):
        user = get_object_or_404(User, username=username)
        if (
            not (
                token_in_cache := cache.cache.get(
                    f"activate_token_user_{user.username}"
                )
            )
            or token_in_cache != token
        ):
            return response.HttpResponse("Your link has expired!", status=400)

        user.is_active = True
        user.save(update_fields=["is_active"])

        # login:
        login(self.request, user)
        cache.cache.delete(f"activate_token_user_{user.username}")

        return render(request, self.template_name)


class ProfileView(DetailView, LoginRequiredMixin):
    model = User
    template_name = "auth/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["user"]
        address = Address.objects.filter(user=user)
        context["address"] = address
        order_completed = Order.objects.filter(user=user, status=True)
        order_incompleted = Order.objects.filter(user=user, status=False)
        context["order_completed"] = order_completed
        context["order_incompleted"] = order_incompleted
        return context


class LogoutView(generic.RedirectView):
    url = "/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(self.request, *args, **kwargs)


class EditProfile(generic.RedirectView):
    model = User
    template_name = "auth/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"]
        return context

    def post(self, request):
        username = self.request.POST.get("username")
        first_name = self.request.POST.get("first_name")
        last_name = self.request.POST.get("last_name")
        email = self.request.POST.get("email")
        phone_number = self.request.POST.get("phone_number")
        gender = self.request.POST.get("gender")
        data = {
            "first_name": first_name,
            "gender": gender,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "username": username,
        }
        User.objects.filter(email=email).update(**data)
        login(self.request, request.user)
        success = " change successfully."
        return HttpResponse(success)


class ActivateProfile(generic.RedirectView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            if not user.is_active:
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
        return redirect("profile", User.objects.get(email=user.email).slug)


class Changepassword(generic.RedirectView):
    def post(self, request):
        user = request.user
        password = self.request.POST.get("backpassword")
        newpassword = self.request.POST.get("newpassword")
        newconfirmpassword = self.request.POST.get("newconfirmpassword")
        if user.check_password(password):
            if newpassword == newconfirmpassword:
                user.set_password(newpassword)
                user.save()
                login(self.request, user)
                success = "password change succeddfully."
                return HttpResponse(success)
            else:
                success = "password and new password not match."
                return HttpResponse(success)
        else:
            success = "back password is not correct."
            return HttpResponse(success)


class ForgotPassword(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        if not cache.get_or_create(
            f"activate_token_user_{user.username}", lambda: uuid4().hex, 180
        ):
            # send mail !
            mail.send_mail(
                f"Verification {user.username}",
                user.email,
                "auth/forgot_password.html",
                {
                    "user": user,
                    "token": cache.cache.get(f"activate_token_user_{user.username}"),
                    "host": self.request.get_host(),
                },
            )
            login(self.request, user)
            return redirect("email-change-password")
        return response.HttpResponse("THE LINK HAS BEEN PREVIOSLY SENT.")


class ChangePasswordForgot(generic.View):
    template_name = "auth/changepasswordpage.html"

    def get(self, request, username, token):
        context = {"token": token, "username": username}
        return render(request, self.template_name, context)

    def post(self, request, username, token):
        user = User.objects.get(username=username)
        if (
            not (
                token_in_cache := cache.cache.get(
                    f"activate_token_user_{user.username}"
                )
            )
            or token_in_cache != token
        ):
            return response.HttpResponse("Your link has expired!", status=400)

        newpassword = self.request.POST.get("newpassword")
        newconfirmpassword = self.request.POST.get("newconfirmpassword")
        if newpassword == newconfirmpassword:
            user.set_password(newpassword)
            user.save()
            login(self.request, user)
            cache.cache.delete(f"activate_token_user_{user.username}")
            return redirect("success-change-password", user.slug)
        else:
            return response.HttpResponse("password is not match", status=400)


class CreateAddress(generic.RedirectView):
    def post(self, request):
        user = request.user
        first_name_recivier = self.request.POST.get("first_name_recivier")
        last_name_recivier = self.request.POST.get("last_name_recivier")
        province = self.request.POST.get("province")
        zip = self.request.POST.get("zip")
        city = self.request.POST.get("city")
        apartment_address = self.request.POST.get("apartment_address")
        phone_number_reciver = self.request.POST.get("phone_number_reciver")
        address = Address.objects.create(
            user=user,
            first_name_recivier=first_name_recivier,
            last_name_recivier=last_name_recivier,
            city=city,
            province=province,
            apartment_address=apartment_address,
            zip=zip,
            phone_number_reciver=phone_number_reciver,
        )
        address.save()
        success = "your Address registration."
        return HttpResponse(success)


class UpdateAddress(generic.RedirectView):
    template_name = "auth/updateaddress.html"

    def get(self, request, id):
        address = Address.objects.filter(id=id, user=request.user)
        return render(request, self.template_name, {"address": address})

    def post(self, request, id):
        user = request.user
        first_name_recivier = self.request.POST.get("first_name_recivier")
        last_name_recivier = self.request.POST.get("last_name_recivier")
        province = self.request.POST.get("province")
        zip = self.request.POST.get("zip")
        city = self.request.POST.get("city")
        apartment_address = self.request.POST.get("apartment_address")
        phone_number_reciver = self.request.POST.get("phone_number_reciver")
        Address.objects.filter(user=user, id=id).update(
            first_name_recivier=first_name_recivier,
            last_name_recivier=last_name_recivier,
            city=city,
            province=province,
            apartment_address=apartment_address,
            zip=zip,
            phone_number_reciver=phone_number_reciver,
        )
        login(self.request, request.user)
        success = " change successfully."
        return HttpResponse(success)
