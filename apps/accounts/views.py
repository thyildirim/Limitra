from datetime import timedelta

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from apps.accounts.models import Account
from apps.accounts.serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow any user


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now() + timedelta(hours=3) # Now + 3 hours
        user.save(update_fields=['last_login'])
        return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

    
