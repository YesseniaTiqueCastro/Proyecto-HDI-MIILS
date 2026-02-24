from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import traceback

from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, GESTION_INSPECCION_ENDPOINT
from app.db.dependencies import get_db
from app.repositories.api_hdi_repository import ApiHDIRepository

router = APIRouter(
    prefix="/inspection",
    tags=["Inspection"]
)


def to_iso(value):
    """
    Convierte datetime a string ISO requerido por HDI
    """
    if not value:
        return None
    if isinstance(value, datetime):
        return value.isoformat() + "Z"
    return value


def _gestionar_inspeccion_logica(
    id_inspeccion: str,
    data: dict,
    db: Session
):

    token = obtener_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # ===============================
    # TRAER DATA DESDE BD
    # ===============================
    api_hdi = ApiHDIRepository.get_by_inspeccion(
        db=db,
        id_service=id_inspeccion
    )

    if not api_hdi:
        return 404, {
            "detalle": f"No existe información HDI para {id_inspeccion}"
        }

    # ===============================
    # VEHICULO VIENE DEL FRONT
    # ===============================
    vehiculo_front = data.get("inspeccion", {}).get("vehiculo", {})

    # ===============================
    # MAPEO CORRECTO CAMPOS BD -> HDI
    # (USAMOS .get PARA EVITAR ERRORES
    #  DE COLUMNAS FALTANTES)
    # ===============================
    inspeccion = {
        "id_inspeccion": int(id_inspeccion),
        "usuarioCreador": "COLSERAUTO",
        "fechaHoraInspeccion": to_iso(api_hdi.get("initial_time")),
        "fechaHoraSalidaInspeccion": to_iso(api_hdi.get("final_time")),
        "tipo": api_hdi.get("tipo"),
        "codigoFasecolda": api_hdi.get("codigo_fasecolda"),
        "servicio": api_hdi.get("servicio"),
        "chasis": api_hdi.get("numero_chasis"),
        "serial": api_hdi.get("numero_serie"),
        "motor": api_hdi.get("numero_motor"),
        "modelo": int(api_hdi["modelo"]) if api_hdi["modelo"] else None,
        "color": api_hdi.get("color"),
        "tipoCarroceria": api_hdi.get("carroceria"),
        "tipoVehiculo": api_hdi.get("tipo_vehiculo"),

        "vehiculo": vehiculo_front
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
            "inspeccion": inspeccion,
            "calificaciones": [],
            "accesorios": [],
            "comentarios": [],
            "aprobacion": {
                "identificacion": {
                    "tipoDocumento": "CC",
                    "numeroDocumento": "12345678",
                    "aprobado": True
                },
                "operario": {
                    "usuario": "COLSERAUTO",
                    "aprobado": True
                }
            }
        }
    }

    print("===== BODY ENVIADO A HDI =====")
    print(body)

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{GESTION_INSPECCION_ENDPOINT}/{id_inspeccion}",
        headers=headers,
        json=body
    )

    print("HDI STATUS:", response.status_code)
    print("HDI RESPONSE:", response.text)

    try:
        response_json = response.json()
    except Exception:
        response_json = {"raw": response.text}

    return response.status_code, response_json


@router.post("/{id_inspeccion}")
def gestionar_inspeccion(
    id_inspeccion: str,
    payload: dict,
    db: Session = Depends(get_db)
):
    try:
        status, data = _gestionar_inspeccion_logica(
            id_inspeccion=id_inspeccion,
            data=payload,
            db=db
        )

        return {
            "status": status,
            "response": data
        }

    except Exception as e:
        print("ERROR REAL BACKEND:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))