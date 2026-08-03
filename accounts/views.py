from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserRegistrationSerializer
from .auth_serializers import EmailTokenObtainPairSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class EmailLoginAPIView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer