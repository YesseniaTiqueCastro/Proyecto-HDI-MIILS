from sqlalchemy import text
from sqlalchemy.orm import Session

class ApiHDIRepository:

    @staticmethod
    def get_by_inspeccion(
        db: Session,
        id_service: str | None = None
    ):
        query = """
        SELECT
            id_service,
            service_type,
            tipo,
            servicio,
            tipo_vehiculo,
            initial_time,
            final_time,
            modelo,
            numero_chasis,
            numero_motor,
            numero_serie,
            color,
            carroceria,
            kilometraje,
            tipo_caja,
            codigo_fasecolda
        FROM api_hdi
        WHERE id_service = :id_service
        """

        result = (
            db.execute(text(query), {"id_service": id_service})
            .mappings()
            .first()
        )

        return result