from public.views import template
from django.urls import path

urlpatterns = [
    path("", template.HomeView.as_view(), name="home"),
    path("Aboutus/", template.AboutView.as_view(), name="about"),
    path(
        "Contact_us/",
        template.ContactUs.as_view(),
        name="contact",
    ),

]
