from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, ValidateUserSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # Use this for JSON responses


class RegisterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginUserView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ValidateUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



def user_login(request):
    return render(request, 'auth/login.html')


@login_required()
def user_logout(request):
    # Blacklist the user's refresh token if it exists
    if request.user.is_authenticated:
        try:
            # Get the refresh token from the request's cookies or headers
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception as e:
            # Log the exception or pass if blacklisting is not necessary
            pass
    
    # Log the user out from the session
    logout(request)
    
    # Redirect to the 'user_login' view in the 'users' app
    return JsonResponse({"message": "User logged out."}, status=200)