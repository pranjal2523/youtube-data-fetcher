# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch-youtube-data/', views.YouTubeDataAPIView.as_view(), name='fetch-youtube-data'),

]
