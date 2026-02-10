from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependencias que provee una sesión de base de datos
    y garantiza su cierre correcto.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

