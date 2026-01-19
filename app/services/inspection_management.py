from datetime import datetime
import uuid

from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import (
    HDI_BASE_URL,
    GESTION_INSPECCION_ENDPOINT,
    USE_HDI_MOCK
)

USUARIO_PROVEEDOR = "WS_COLSERAUTO"


# =========================
# Helpers
# =========================

def construir_aprobacion(aprobado: bool, razon_rechazo: int | None):
    return {
        "aprobado": aprobado,
        "razonRechazo": None if aprobado else razon_rechazo
    }


def construir_info_request():
    return {
        "requestID": str(uuid.uuid4()),
        "fecha": datetime.utcnow().isoformat() + "Z",
        "aplicacionCliente": "12",
        "terminal": "Colserauto",
        "ip": "1.1.1.1"
    }


# =========================
# MOCK
# =========================

def mock_gestionar_inspeccion(id_inspeccion):
    return 200, {
        "success": True,
        "message": "Gestión de inspección procesada exitosamente (MOCK)",
        "data": {
            "idInspeccion": id_inspeccion,
            "estado": "GESTIONADA",
            "fechaProcesamiento": datetime.utcnow().isoformat() + "Z"
        }
    }




def gestionar_inspeccion(
    id_inspeccion: str,
    inspeccion: dict,
    aprobacion_identificacion: bool,
    razon_identificacion: int | None,
    aprobacion_operario: bool,
    razon_operario: int | None,
    calificaciones: list | None = None,
    accesorios: list | None = None,
    comentarios: list | None = None
):
    """
    Gestiona una inspección de HDI.
    método es reutilizable para HDI / HALCON.
    """

    if USE_HDI_MOCK:
        return mock_gestionar_inspeccion(id_inspeccion)

    token = obtener_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "infoRequest": construir_info_request(),
        "solicitud": {
            "operacion": "GESTIONAR",
            "lineaNegocio": "AUTOS",
            "inspeccion": {
                "usuarioCreador": USUARIO_PROVEEDOR,
                **inspeccion
            },
            "calificaciones": calificaciones or [],
            "accesorios": accesorios or [],
            "comentarios": comentarios or [],
            "aprobacion": {
                "identificacion": construir_aprobacion(
                    aprobado=aprobacion_identificacion,
                    razon_rechazo=razon_identificacion
                ),
                "operario": construir_aprobacion(
                    aprobado=aprobacion_operario,
                    razon_rechazo=razon_operario
                )
            }
        }
    }

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{GESTION_INSPECCION_ENDPOINT}/{id_inspeccion}",
        headers=headers,
        json=body
    )
    
    return response.status_code, response.json()
    
