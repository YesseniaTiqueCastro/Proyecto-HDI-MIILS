from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, HEALTH_ENDPOINT

def health_check():
    token = obtener_token()

    headers = {
        "Authorization": f"Bearer {token}",
        
    }

    response = HDIClient.get(
        url=f"{HDI_BASE_URL}{HEALTH_ENDPOINT}",
        headers=headers
    )

    return response.status_code, response.json()
