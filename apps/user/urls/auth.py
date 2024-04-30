from django.urls import path
from django.views.generic import TemplateView
from apps.user.views import api, template

urlpatterns = [
    path(
        "verification/<str:username>/<str:token>",
        template.VerificationView.as_view(),
        name="verification",
    ),
    path("signup/", api.RegisterView.as_view(), name="signup"),
    path("login/", api.LoginView.as_view(), name="login"),
    path("login_otp/", api.LoginViewOtp.as_view(), name="loginotp"),
    path("otp/<str:token>/", api.ConfirmOtp.as_view(), name="confirmotp"),
    path(
        "send_email/",
        TemplateView.as_view(template_name="auth/send_email.html"),
        name="send_email",
    ),
]
