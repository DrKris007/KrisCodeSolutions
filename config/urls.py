"""Root URL configuration."""
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from website.sitemaps import StaticViewSitemap

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": StaticViewSitemap}}, name="sitemap"),
    path("", include("website.urls")),
]

if settings.SERVE_MEDIA_FILES:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
