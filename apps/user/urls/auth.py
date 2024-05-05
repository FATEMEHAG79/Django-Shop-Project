from django.urls import path
from django.views.generic import TemplateView
from apps.user.views import api, template

urlpatterns = [
    path(
        "verification/<str:username>/<str:token>",
        template.VerificationView.as_view(),
        name="verification",
    ),
    path("login/", api.SendOtp.as_view(), name="signup/in"),
    path("login/", api.LoginView.as_view(), name="login"),
    path("login/<str:email>/<str:token>", api.ConfirmOtp.as_view(), name="confirmotp"),
    path(
        "Register/<str:email>/<str:token>",
        api.ConfirmOtpRegister.as_view(),
        name="confirmotpregister",
    ),
    path("Register/<str:email>/", api.Registeration.as_view(), name="register"),
    path(
        "send_email/",
        TemplateView.as_view(template_name="auth/send_email.html"),
        name="send_email",
    ),
]
