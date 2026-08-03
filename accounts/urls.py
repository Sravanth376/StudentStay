from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationAPIView,
    EmailLoginAPIView,
)

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),

    path("login/", EmailLoginAPIView.as_view(), name="login"),

    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]