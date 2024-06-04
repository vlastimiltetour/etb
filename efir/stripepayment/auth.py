import requests
from django.conf import settings


def get_oauth_token():
    url = settings.ACCESS_TOKEN_URL
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "scope": settings.SCOPE,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]
