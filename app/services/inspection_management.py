from fastapi import APIRouter, HTTPException
from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, GESTION_INSPECCION_ENDPOINT
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/inspection",
    tags=["Inspection"]
)


def _gestionar_inspeccion_logica(
    id_inspeccion: str,
    data: dict
):
    """
    Envía gestión completa de inspección a HDI
    """

    token = obtener_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "infoRequest": {
            "requestID": str(uuid.uuid4()),
            "fecha": datetime.utcnow().isoformat() + "Z",
            "aplicacionCliente": "12",
            "terminal": "Colserauto",
            "ip": "1.1.1.1"
        },
        "solicitud": {
            "operacion": "GESTIONAR",
            "lineaNegocio": "AUTOS",
            "inspeccion": data["inspeccion"],
            "calificaciones": data.get("calificaciones", []),
            "accesorios": data.get("accesorios", []),
            "comentarios": data.get("comentarios", []),
            "aprobacion": data.get("aprobacion", {})
        }
    }

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{GESTION_INSPECCION_ENDPOINT}/{id_inspeccion}",
        headers=headers,
        json=body
    )

    return response.status_code, response.json()


@router.post("/{id_inspeccion}")
def gestionar_inspeccion(
    id_inspeccion: str,
    payload: dict
):
    """
    Gestiona inspección completa HDI
    """

    try:
        status, data = _gestionar_inspeccion_logica(
            id_inspeccion=id_inspeccion,
            data=payload
        )

        return {
            "status": status,
            "response": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))