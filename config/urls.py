from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include

urlpatterns = i18n_patterns(
    path("", include("public.urls")),
    path("", include("apps.user.urls")),
    prefix_default_language=False,
)
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += (
        [path("admin/", admin.site.urls)]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )