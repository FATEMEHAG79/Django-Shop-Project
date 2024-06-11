from django.urls import path
from django.views.generic import TemplateView
from apps.user.views import authenticate, template

urlpatterns = [
    path(
        "verification/<str:username>/<str:token>",
        template.VerificationView.as_view(),
        name="verification",
    ),
    path("profile/", authenticate.SendOtp.as_view(), name="signup/in"),
    path("profile/login/", authenticate.LoginView.as_view(), name="login"),
    path("profile/confirmotp/", authenticate.ConfirmOtp.as_view(), name="confirmotp"),
    path(
        "profile/confirmregistration/",
        authenticate.ConfirmOtpRegister.as_view(),
        name="confirmregistration",
    ),
    path(
        "profile/register/<str:email>",
        authenticate.Registeration.as_view(),
        name="register",
    ),
    path(
        "send_email/",
        TemplateView.as_view(template_name="auth/send_email.html"),
        name="send_email",
    ),
    path(
        "email-change-password/",
        TemplateView.as_view(template_name="auth/email-password-change.html"),
        name="email-change-password",
    ),
    path(
        "success-change-password/<str:slug>",
        TemplateView.as_view(template_name="auth/changepassword_successful.html"),
        name="success-change-password",
    ),
    path("profile/view/<str:slug>/", template.ProfileView.as_view(), name="profile"),
    path("logout/", template.LogoutView.as_view(), name="logout"),
    path("profile/view/", template.EditProfile.as_view(), name="editprofile"),
    path("active/", template.ActivateProfile.as_view(), name="activeprofile"),
    path("changepassword/", template.Changepassword.as_view(), name="changepassword"),
    path("forgotpassword/", template.ForgotPassword.as_view(), name="forgotpassword"),
    path(
        "newpassword/<str:username>/<str:token>",
        template.ChangePasswordForgot.as_view(),
        name="newpassword",
    ),
]
