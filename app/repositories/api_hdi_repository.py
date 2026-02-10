from sqlalchemy import text
from sqlalchemy.orm import Session


class ApiHDIRepository:

    @staticmethod
    def get_by_placa_or_inspeccion(
        db: Session,
        placa: str | None = None,
        id_service: int | None = None
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
            color_front,
            color_id_hdi,
            carroceria,
            carroceria_id_hdi,
            kilometraje,
            tipo_caja,
            id_caja_hdi,
            codigo_fasecolda
        FROM api_hdi
        WHERE 1=1
        """

        params = {}

        if placa:
            query += " AND placa = :placa"
            params["placa"] = placa

        if id_service:
            query += " AND id_service = :id_service"
            params["id_service"] = id_service

        result = (
            db.execute(text(query), params)
            .mappings()
            .first()
        )

        return result
