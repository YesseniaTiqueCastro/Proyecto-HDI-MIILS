from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL
import uuid
from datetime import datetime


UPLOAD_PHOTOS_ENDPOINT = "/management-inspections/uploadphotos"


def generar_presigned_url_fotos(
    id_inspeccion: str,
    usuario: str
):
    """
    Genera la URL presigned para subir el ZIP de fotos
    """

    token = obtener_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "idInspector": usuario,
        "Content-Type": "application/json"
    }

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{UPLOAD_PHOTOS_ENDPOINT}/{id_inspeccion}",
        headers=headers
    )

    return response.status_code, response.json()
