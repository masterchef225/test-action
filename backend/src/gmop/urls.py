from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import gmop.authentication.urls as auth_urls
from gmop.core.swagger import urlpatterns as swagger_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(auth_urls, namespace="authentication")),
]

urlpatterns += swagger_urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
