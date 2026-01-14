from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, GESTION_INSPECCION_ENDPOINT
from datetime import datetime
import uuid


def gestionar_inspeccion(
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
            "calificaciones": [],
            "aprobacion": {
                "identificacion": {
                    "aprobado": False,
                    "razonRechazo": 35
                },
                "operario": {
                    "aprobado": False,
                    "razonRechazo": 2
                }
            }
        }
    }

    response = HDIClient.post(
        url=f"{HDI_BASE_URL}{GESTION_INSPECCION_ENDPOINT}/{id_inspeccion}",
        headers=headers,
        json=body
    )

    return response.status_code, response.json()
