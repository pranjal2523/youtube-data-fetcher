# users/urls.py
from django.urls import path
from .views import highlevel, youtube

urlpatterns = [

    path('home', youtube.home, name='home'),
    path('fetch-youtube-data/', youtube.YouTubeDataAPIView.as_view(), name='fetch-youtube-data'),
    
    
    
    
    
    
    
    path('initiate-auth/', highlevel.initiate_auth, name='initiate_auth'),
    path('oauth/callback/', highlevel.oauth_callback, name='oauth_callback'),
    path('custom-fields/', highlevel.CustomFieldsAPIView.as_view(), name='custom-fields'),
]
