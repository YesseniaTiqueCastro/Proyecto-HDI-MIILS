from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import traceback

from app.db.dependencies import get_db
from app.repositories.api_hdi_repository import ApiHDIRepository
from app.repositories.calificaciones_repository import CalificacionesRepository
from app.repositories.accesorios_repository import AccesoriosRepository

router = APIRouter(
    prefix="/inspection",
    tags=["Inspection Management"]
)


# ==========================================================
# ENDPOINT GESTIÓN CONSUME VISTAS HALCÓN
# ==========================================================

@router.get("/{id_inspeccion}")
def gestionar_inspeccion(
    id_inspeccion: str,
    db: Session = Depends(get_db)
):
    try:

        # ==========================================
        #  CONSULTAR VISTA api_hdi (GCP)
        # ==========================================
        api_hdi = ApiHDIRepository.get_by_inspeccion(
            db=db,
            id_service=id_inspeccion
        )

        if not api_hdi:
            raise HTTPException(
                status_code=404,
                detail="Inspección no encontrada en base de datos"
            )

        # ==========================================
        #  CONSULTAR VISTA api_calificaciones
        # ==========================================
        calificaciones = CalificacionesRepository.get_by_inspeccion(
            db=db,
            id_service=id_inspeccion
        )

        # ==========================================
        # CONSULTAR VISTA api_accesorios
        # ==========================================
        accesorios = AccesoriosRepository.get_by_inspeccion(
            db=db,
            id_service=id_inspeccion
        )

        # ==========================================
        # RESPUESTA COMPLETA PARA EL FRONT
        # ==========================================

        response = {
            "inspeccion": {
                "fechaHoraInspeccion": api_hdi.get("initial_time"),
                "fechaHoraSalidaInspeccion": api_hdi.get("final_time"),
                "servicio": api_hdi.get("servicio"),
                "chasis": api_hdi.get("numero_chasis"),
                "serial": api_hdi.get("numero_serie"),
                "motor": api_hdi.get("numero_motor"),
                "modelo": api_hdi.get("modelo"),
                "color": api_hdi.get("color_id_hdi"),
                "tipoCarroceria": api_hdi.get("carroceria_id_hdi"),
                "tipoVehiculo": api_hdi.get("service_type"),
                "kilometraje": api_hdi.get("kilometraje"),
                "caja": api_hdi.get("id_caja_hdi"),
                "tipo": api_hdi.get("tipo"),
                "codigoFasecolda": api_hdi.get("codigo_fasecolda")
            },
            "calificaciones": calificaciones or [],
            "accesorios": accesorios or []
        }

        return response

    except HTTPException:
        raise

    except Exception as e:
        print("ERROR REAL BACKEND:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))