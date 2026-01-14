from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL


UPLOAD_STATUS_ENDPOINT = "/management-inspections/uploadphotos/status"


def consultar_estado_cargue_fotos(
    id_inspeccion: str,
    usuario: str
):
    """
    Consulta el estado del cargue y validación de fotos de una inspección
    """

    token = obtener_token() 

    headers = {
        "Authorization": f"Bearer {token}",
        "idInspector": usuario,
        "Content-Type": "application/json"
    }

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{UPLOAD_STATUS_ENDPOINT}/{id_inspeccion}",
        headers=headers
    )

    return response.status_code, response.json()
