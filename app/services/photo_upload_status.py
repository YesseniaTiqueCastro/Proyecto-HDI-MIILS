from fastapi import APIRouter, Query, HTTPException
from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL

UPLOAD_STATUS_ENDPOINT = "/management-inspections/uploadphotos/status"

router = APIRouter(
    prefix="/photos",
    tags=["Photos"]
)

def _consultar_estado_cargue_fotos_logica(
    id_inspeccion: str,
    usuario: str
):
    """
    Lógica pura HDI: consulta el estado del cargue y validación de fotos
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


@router.get("/upload-status")
def consultar_estado_cargue_fotos(
    id_inspeccion: str = Query(..., description="ID de la inspección"),
    usuario: str = Query(..., description="Usuario inspector")
):
    """
    Endpoint FastAPI para consultar estado de cargue de fotos
    """
    try:
        status_code, data = _consultar_estado_cargue_fotos_logica(
            id_inspeccion=id_inspeccion,
            usuario=usuario
        )
        return {
            "status": status_code,
            "response": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
