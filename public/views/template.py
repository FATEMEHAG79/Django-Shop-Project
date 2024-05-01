from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views import generic
from django.conf import settings


class HomeView(generic.TemplateView):
    template_name = "public/home.html"


class AboutView(generic.TemplateView):
    template_name = "public/about.html"


class ContactUs(generic.TemplateView):
    template_name = "public/contactus.html"

    def post(self, request):
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        subject = request.POST.get("subject", None)
        message = request.POST.get("message", None)
        if not all((name, email, email, subject, message)):
            messages.info(request, "This field should not be null ! ")
            return redirect("contact")
        msg = f"name : {name} \n email : {email} \n subject : {subject} \n message : {message}"
        send_mail(
            subject,
            msg,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        msg_confirm = (
            f"Hi {name}👋!\n THank you for send email for us & visit my site ."
        )
        send_mail(
            "confim email contact us",
            msg_confirm,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.info(
            request, "   your email sent successfully! please check your email. "
        )
        return redirect("contact")
