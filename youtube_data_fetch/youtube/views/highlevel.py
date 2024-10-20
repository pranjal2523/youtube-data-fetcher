
from django.shortcuts import redirect
from django.conf import settings
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from youtube.models import Token


def initiate_auth(request):
    # Define the options
    options = {
        "requestType": "code",
        "redirectUri": "http://localhost:8000/oauth/callback/",
        "clientId": settings.CLIENT_ID,  # Replace with actual clientId or load from settings
        "scopes": [
            "contacts.readonly",
            "contacts.write"
        ]
    }

    # Construct the redirect URL
    base_url = f"{settings.OAUTH_URL}/oauth/chooselocation"
    query_params = (
        f"response_type={options['requestType']}&"
        f"redirect_uri={options['redirectUri']}&"
        f"client_id={options['clientId']}&"
        f"scope={' '.join(options['scopes'])}"
    )
    redirect_url = f"{base_url}?{query_params}"

    # Redirect to the constructed URL
    return redirect(redirect_url)


@csrf_exempt
def oauth_callback(request):
    # Check if 'code' parameter is present in the request
    authorization_code = request.GET.get('code')
    if not authorization_code:
        return JsonResponse({'error': 'Authorization code is missing'}, status=400)

    # Prepare the data for the POST request
    data = {
        'client_id': settings.CLIENT_ID,  # Replace with appConfig.clientId
        'client_secret': settings.CLIENT_SECRET,  # Replace with appConfig.clientSecret
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'user_type': 'Location',
        'redirect_uri': 'http://localhost:3000/oauth/callback'
    }

    # Set the headers for the request
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Perform the POST request to exchange the authorization code for an access token
    try:
        response = requests.post(
            'https://services.leadconnectorhq.com/oauth/token',
            data=data,
            headers=headers
        )
        response_data = response.json()
        
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')

        if Token.objects.all():
            Token.objects.update(
                access_token=access_token,
                refresh_token=refresh_token
            )
        else:
            Token.objects.create(
                access_token=access_token,
                refresh_token=refresh_token
            )
        
        print(response_data)
    except requests.RequestException as e:
        return JsonResponse({'error': 'Request failed', 'details': str(e)}, status=500)

    # Return the response data as JSON
    return JsonResponse({'data': response_data})


def generate_refresh_token(refresh_token):
    # Configuration details
    client_id = settings.CLIENT_ID  # Replace with actual client ID
    client_secret = settings.CLIENT_SECRET  # Replace with actual client secret
    redirect_uri = 'http://localhost:3000/oauth/callback'
    url = 'https://services.leadconnectorhq.com/oauth/token'

    # Data for the POST request
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'user_type': 'Location',
        'redirect_uri': redirect_uri
    }

    # Headers for the request
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        # Perform the POST request to obtain the new access token
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()
         
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')

        if Token.objects.all():
            Token.objects.update(
                access_token=access_token,
                refresh_token=refresh_token
            )
        else:
            Token.objects.create(
                access_token=access_token,
                refresh_token=refresh_token
            )
        print(response_data)
        return response_data
    except requests.RequestException as e:
        # Handle request exceptions
        return {'error': 'Request failed', 'details': str(e)}
    

class CustomFieldsAPIView(APIView):
    def get(self, request):
        url = "https://stoplight.io/mocks/highlevel/integrations/39582857/locations/ve9EPM428h8vShlRW1KT/customFields"
        querystring = {"model": "contact"}
        token = Token.objects.all().first().access_token
        token = "Bearer " + str(token)
        headers = {
            "Authorization": token,
            "Version": "2021-07-28",
            "model": "contact",
            "Prefer": "code=200, dynamic=true",
            "Accept": "application/json"
        }
        
        # Make the external API request
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)