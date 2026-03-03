from sqlalchemy.orm import Session
from sqlalchemy import text


class CalificacionesRepository:

    @staticmethod
    def get_by_inspeccion(db: Session, id_service: str):

        query = text("""
            SELECT *
            FROM vista_calificaciones
            WHERE id_service = :id
        """)

        result = db.execute(query, {"id": id_service}).fetchall()

        return [dict(row._mapping) for row in result]