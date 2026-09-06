from rest_framework import generics
from apps.accounts.models import Account
from apps.accounts.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
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
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)

    
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  
    
    def post(seşf,request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

    
