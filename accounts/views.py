from rest_framework import generics
from .models import User
from .serializers import UserRegistrationSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer