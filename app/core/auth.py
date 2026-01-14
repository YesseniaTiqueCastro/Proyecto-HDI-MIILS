from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, TOKEN_ENDPOINT
import os
def obtener_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("HDI_CLIENT_ID"),
        "client_secret": os.getenv("HDI_CLIENT_SECRET")
    }

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{TOKEN_ENDPOINT}",
        headers=headers,
        data=data
    )

    response.raise_for_status()
    return response.json()["access_token"]










