from django.conf import settings
from django.urls import include, path

from .admin import admin_site

urlpatterns = [
    path("", include("cookie.trails.urls")),
    path("admin/", admin_site.urls),
]


if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
