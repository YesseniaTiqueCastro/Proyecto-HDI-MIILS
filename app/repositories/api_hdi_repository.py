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
            initial_time,
            final_time,
            modelo,
            numero_chasis,
            numero_motor,
            numero_serie,
            color_front,
            color_id_hdi,
            carroceria_id_hdi,
            kilometraje,
            id_caja_hdi,
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