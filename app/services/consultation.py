from fastapi import APIRouter, Query, HTTPException
from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, CONSULTA_INSPECCION_ENDPOINT
from datetime import datetime
import uuid

router = APIRouter(prefix="/consultation", tags=["Consultation"])


def _consultar_inspeccion_logica(
    id_inspeccion: str | None = None,
    placa: str | None = None
):
    token = obtener_token()

    if not id_inspeccion and not placa:
        raise ValueError("Debes consultar por id_inspeccion o placa")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "crearInspMIILSRq": {
            "infoRequest": {
                "requestID": str(uuid.uuid4()),
                "fecha": datetime.utcnow().isoformat() + "Z",
                "aplicacionCliente": "WS_COLSERAUTO",
                "terminal": "WS_COLSERAUTO",
                "ip": "1.1.1.1"
            },
            "solicitud": {
                "operacion": "CONSULTAR",
                "lineaNegocio": "AUTOS",
                "inspeccion": {}
            }
        }
    }

    if id_inspeccion:
        body["crearInspMIILSRq"]["solicitud"]["inspeccion"]["idInspeccion"] = id_inspeccion

    if placa:
        body["crearInspMIILSRq"]["solicitud"]["inspeccion"]["placa"] = placa

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{CONSULTA_INSPECCION_ENDPOINT}",
        headers=headers,
        json=body
    )

    response_json = response.json()

    root = response_json.get("crearConsultarInspMIILSRs", {})
    solicitud = root.get("solicitud", {})
    inspeccion = solicitud.get("inspeccion", {})
    datos_auto = inspeccion.get("datosInspeccionAuto", {})
    vehiculo = datos_auto.get("vehiculo", {})

    consulta_siniestros = vehiculo.get("consultaSiniestros", {})
    siniestros_raw = consulta_siniestros.get("siniestros")

    if siniestros_raw in [None, "null", "None"]:
        siniestros = []
    elif isinstance(siniestros_raw, list):
        siniestros = siniestros_raw
    elif isinstance(siniestros_raw, dict):
        siniestros = [siniestros_raw]
    else:
        siniestros = []

    return {
        "inspeccion": inspeccion,
        "vehiculo": vehiculo,
        "siniestros": siniestros,
        "raw_response": response_json
    }


@router.get("/consultar")
def consultar_inspeccion(
    id_inspeccion: str | None = Query(None, description="ID de la inspección"),
    placa: str | None = Query(None, description="Placa del vehículo")
):
    try:
        return _consultar_inspeccion_logica(id_inspeccion, placa)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
