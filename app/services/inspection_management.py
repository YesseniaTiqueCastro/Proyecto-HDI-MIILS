from fastapi import APIRouter, HTTPException
from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, GESTION_INSPECCION_ENDPOINT
from datetime import datetime
import uuid

router = APIRouter()

def _gestionar_inspeccion_logica(
    id_inspeccion,
    usuario,
    fecha_hora_inspeccion,
    fecha_hora_salida_inspeccion
):
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
            "inspeccion": {
                "usuarioCreador": usuario,
                "fechaHoraInspeccion": fecha_hora_inspeccion,
                "fechaHoraSalidaInspeccion": fecha_hora_salida_inspeccion
            }
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
    usuario: str,
    fecha_hora_inspeccion: str,
    fecha_hora_salida_inspeccion: str
):
    try:
        status, data = _gestionar_inspeccion_logica(
            id_inspeccion,
            usuario,
            fecha_hora_inspeccion,
            fecha_hora_salida_inspeccion
        )
        return {
            "status": status,
            "response": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
