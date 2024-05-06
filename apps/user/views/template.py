from utils import cache
from django.http import response
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView

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
    template_name = 'auth/profile.html'
    login_url = 'login'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user']
        return context



class LogoutView(generic.RedirectView):
    url = "/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(self.request, *args, **kwargs)