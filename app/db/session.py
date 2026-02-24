from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

USE_SSL = os.getenv("DB_SSL", "false").lower() == "true"

connect_args = {}

if USE_SSL:
    connect_args = {
        "sslmode": "verify-full",
        "sslrootcert": os.getenv("DB_SSL_ROOT_CERT"),
        "sslcert": os.getenv("DB_SSL_CERT"),
        "sslkey": os.getenv("DB_SSL_KEY"),
    }

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()