from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views import generic
from django.conf import settings


class HomeView(generic.TemplateView):
    template_name = "public/home.html"



class AboutView(generic.TemplateView):
    template_name = "public/about.html"
