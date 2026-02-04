from fastapi import APIRouter, HTTPException
from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, HEALTH_ENDPOINT

router = APIRouter()

def _health_check_logica():
    token = obtener_token()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = HDIClient.get(
        url=f"{HDI_BASE_URL}{HEALTH_ENDPOINT}",
        headers=headers
    )

    return response.status_code, response.json()

@router.get("/")
def health_check():
    try:
        status_code, data = _health_check_logica()
        return {
            "status": status_code,
            "response": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
