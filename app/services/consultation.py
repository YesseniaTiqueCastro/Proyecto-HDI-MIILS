from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, CONSULTA_INSPECCION_ENDPOINT
from datetime import datetime
import uuid

def consultar_inspeccion(id_inspeccion=None, placa=None):
    token = obtener_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    if not id_inspeccion and not placa:
        raise ValueError("Debe enviar id_inspeccion o placa")

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
        body["crearInspMIILSRq"]["solicitud"]["inspeccion"]["idInspeccion"] = str(id_inspeccion)

    if placa:
        body["crearInspMIILSRq"]["solicitud"]["inspeccion"]["placa"] = placa

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{CONSULTA_INSPECCION_ENDPOINT}",
        headers=headers,
        json=body
    )

    response_json = response.json()

    resultado = {
        "status": response.status_code,
        "inspeccion": None,
        "vehiculo": None,
        "siniestros": [],
        "raw_response": response_json
    }

    try:
        root = response_json.get("crearConsultarInspMIILSRs", {})
        solicitud = root.get("solicitud", {})
        inspeccion = solicitud.get("inspeccion", {})
        datos_auto = inspeccion.get("datosInspeccionAuto", {})
        vehiculo = datos_auto.get("vehiculo", {})

     
        consulta_siniestros = vehiculo.get("consultaSiniestros", {})
        siniestros_raw = consulta_siniestros.get("siniestros")

        if siniestros_raw in [None, "null", "None"]:
            siniestros_normalizados = []
        elif isinstance(siniestros_raw, list):
            siniestros_normalizados = siniestros_raw
        elif isinstance(siniestros_raw, dict):
            siniestros_normalizados = [siniestros_raw]
        else:
            siniestros_normalizados = []


        resultado["inspeccion"] = inspeccion
        resultado["vehiculo"] = vehiculo
        resultado["siniestros"] = siniestros_normalizados

    except Exception as e:
        resultado["error"] = str(e)

    return response.status_code, resultado
