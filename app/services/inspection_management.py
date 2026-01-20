from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, GESTION_INSPECCION_ENDPOINT, USE_HDI_MOCK
from datetime import datetime
import uuid

USUARIO_PROVEEDOR = "WS_COLSERAUTO"


def construir_aprobacion(aprobado: bool, razon_rechazo: int | None):
    if aprobado:
        return {
            "aprobado": True,
            "razonRechazo": None
        }
    else:
        return {
            "aprobado": False,
            "razonRechazo": razon_rechazo
        }


def mock_gestionar_inspeccion(id_inspeccion):
    request_id = str(uuid.uuid4())

    return 200, {
        "infoResponse": {
            "estado": {
                "codigoEstado": "0",
                "codigoEstadoServidor": "0",
                "descripcionEstado": "Se ejecutó satisfactoriamente la operación solicitada.",
                "severidad": "INFO"
            },
            "requestID": request_id
        },
        "solicitud": {
            "operacion": "GESTIONAR",
            "lineaNegocio": "AUTOS",
            "inspeccion": {
                "estadoInspeccion": "ACTUALIZADA",
                "fechaFinInspeccion": None
            }
        }
    }


def gestionar_inspeccion(
    id_inspeccion,
    fecha_hora_inspeccion,
    fecha_hora_salida_inspeccion,
    aprobacion_identificacion,
    razon_identificacion,
    aprobacion_operario,
    razon_operario,
    calificaciones=None,
    accesorios=None,
    comentarios=None
):
    if USE_HDI_MOCK:
        return mock_gestionar_inspeccion(id_inspeccion)

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
                "usuarioCreador": USUARIO_PROVEEDOR,
                "fechaHoraInspeccion": fecha_hora_inspeccion,
                "fechaHoraSalidaInspeccion": fecha_hora_salida_inspeccion,
                "tipo": 9700,
                "codigoFasecolda": "08002067",
                "servicio": 1,
                "chasis": "9FBC066052L789924",
                "serial": "9FBC066052L789924",
                "motor": "B700F730724",
                "modelo": 2002,
                "color": 0,
                "tipoCarroceria": 6,
                "tipoVehiculo": 1,
                "kilometraje": 170000,
                "kilometrajePorAnio": 8718,
                "tipoPintura": 1,
                "caja": 2
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
