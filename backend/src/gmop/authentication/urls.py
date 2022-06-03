from django.conf.urls import url

from . import views

app_name = "authentication"

urlpatterns = [
    url(r"^obtain_token/$", views.obtain_jwt_token, name="obtain_token"),
    url(r"^refresh_token/$", views.refresh_jwt_token, name="refresh_token"),
]
