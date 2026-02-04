from fastapi import FastAPI

from app.services.health import router as health_router
from app.services.consultation import router as consultation_router
from app.services.inspection_management import router as inspection_router
from app.services.photo_upload import router as photo_upload_router
from app.services.photo_upload_status import router as photo_status_router

app = FastAPI(
    title="API Gestión Inspecciones HDI",
    version="1.0.0"
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(consultation_router, prefix="/consultation", tags=["Consultation"])
app.include_router(inspection_router, prefix="/inspection", tags=["Inspection"])
app.include_router(photo_upload_router, prefix="/photos", tags=["Photos"])
app.include_router(photo_status_router, prefix="/photos", tags=["Photos"])
