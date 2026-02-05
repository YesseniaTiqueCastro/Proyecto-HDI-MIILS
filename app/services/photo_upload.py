from fastapi import APIRouter, Query, HTTPException
from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL

UPLOAD_PHOTOS_ENDPOINT = "/management-inspections/uploadphotos"

router = APIRouter(prefix="/photos", tags=["Photos"])


def _generar_presigned_url_fotos_logica(
    id_inspeccion: str,
    usuario: str
):
    """
    Lógica pura HDI: genera URL presigned para subir ZIP de fotos
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


@router.post("/upload")
def generar_presigned_url_fotos(
    id_inspeccion: str = Query(..., description="ID de la inspección"),
    usuario: str = Query(..., description="Usuario inspector")
):
    """
    Endpoint FastAPI: generar URL presigned para subir fotos
    """
    try:
        status_code, data = _generar_presigned_url_fotos_logica(
            id_inspeccion=id_inspeccion,
            usuario=usuario
        )
        return {
            "status": status_code,
            "response": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
