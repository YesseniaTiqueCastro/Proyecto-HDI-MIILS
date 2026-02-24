from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.health import router as health_router
from app.services.consultation import router as consultation_router
from app.services.inspection_management import router as inspection_router
from app.services.photo_upload import router as photo_upload_router
from app.services.photo_upload_status import router as photo_status_router

app = FastAPI(
    title="API Gestión Inspecciones HDI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health")
app.include_router(consultation_router, prefix="/consultation")
app.include_router(inspection_router)  
app.include_router(photo_upload_router, prefix="/photos")
app.include_router(photo_status_router, prefix="/photos")