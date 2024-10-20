from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    user_login,
    user_logout
)

app_name = "users"

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
]
