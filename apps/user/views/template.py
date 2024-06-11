from uuid import uuid4
from apps.order.models import Order
from utils import cache
from django.http import response
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from utils import mail
from django.shortcuts import redirect
from django.http import JsonResponse

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
        return redirect("profile", User.objects.get(email=email).slug)


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
        return redirect("profile", User.objects.get(user=user).slug)


class Changepassword(generic.RedirectView):
    def post(self, request):
        user = request.user
        password = self.request.POST.get("backpassword")
        newpassword = self.request.POST.get("newpassword")
        newconfirmpassword = self.request.POST.get("newconfirmpassword")
        if user.check_password(password):
            if newpassword==newconfirmpassword:
                user.set_password(newpassword)
                user.save()
                return JsonResponse({"success":True,"message":"password change succeddfully." })
            else:
                return JsonResponse({"success": False, "message": "password and new password not match."})
        else:
            return JsonResponse({"success": False, "message": "back password is not correct."})


