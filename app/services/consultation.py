from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.core.auth import obtener_token
from app.core.client import HDIClient
from app.config.settings import HDI_BASE_URL, CONSULTA_INSPECCION_ENDPOINT
from app.db.session import get_db
from app.repositories.api_hdi_repository import ApiHDIRepository

router = APIRouter(
    prefix="/inspection",
    tags=["Inspection"]
)


def _consultar_inspeccion_logica(
    db: Session,
    id_inspeccion: str | None = None,
    placa: str | None = None
):

    if not id_inspeccion and not placa:
        raise ValueError("Debe enviar id_inspeccion o placa")

    # =====================
    # TOKEN HDI
    # =====================
    token = obtener_token()

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
        body["crearInspMIILSRq"]["solicitud"]["inspeccion"]["idInspeccion"] = str(id_inspeccion)

    if placa:
        body["crearInspMIILSRq"]["solicitud"]["inspeccion"]["placa"] = placa

    # =====================
    # CONSULTA HDI
    # =====================
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

    # =====================
    # EXTRAER PLACA HDI
    # =====================
    placa_hdi = None
    if isinstance(vehiculo.get("placa"), dict):
        placa_hdi = vehiculo.get("placa", {}).get("placa")

    placa_busqueda = placa or placa_hdi

    # =====================
    # CONSULTA BD LOCAL
    # =====================
    data_bd = ApiHDIRepository.get_by_inspeccion(
    db=db,
    id_service=id_inspeccion
)
    # =====================
    # COMPLETAR DESDE BD
    # =====================
    if data_bd:

        vehiculo["tipoCaja"] = data_bd.get("tipo_caja")
        vehiculo["tipoCarroceria"] = data_bd.get("carroceria")
        vehiculo["tipoVehiculo"] = data_bd.get("tipo_vehiculo")
        vehiculo["codigoFasecolda"] = (
            data_bd.get("codigo_fasecolda")
            or vehiculo.get("codigoFasecolda")
        )

        vehiculo["serial"] = data_bd.get("numero_serie")
        vehiculo["color"] = data_bd.get("color")
        vehiculo["kilometraje"] = data_bd.get("kilometraje")

        inspeccion["fechaHoraInspeccion"] = data_bd.get("initial_time")
        inspeccion["fechaHoraSalidaInspeccion"] = data_bd.get("final_time")
        inspeccion["tipo"] = data_bd.get("tipo")
        inspeccion["servicio"] = data_bd.get("servicio")

    return {
        "inspeccion": inspeccion,
        "vehiculo": vehiculo,
        "raw_response": response_json
    }


@router.get("/consultar")
def consultar_inspeccion(
    id_inspeccion: str | None = Query(default=None),
    placa: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    try:
        return _consultar_inspeccion_logica(db, id_inspeccion, placa)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))