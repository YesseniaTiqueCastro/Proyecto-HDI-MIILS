import os
from dotenv import load_dotenv

load_dotenv()

# URL BASE UAT
HDI_BASE_URL = os.getenv(
    "HDI_BASE_URL",
    "https://nonprod-apis-auto.hdiseguros.com.co"
    
    
)


# ENDPOINTS
HEALTH_ENDPOINT = "/vehicle-services/health"
TOKEN_ENDPOINT = "/vehicle-services/token"
CONSULTA_INSPECCION_ENDPOINT = "/vehicle-services/crearConsultarInspMIILS"
GESTION_INSPECCION_ENDPOINT = "/management-inspections/gestionarInspMIILS"
UPLOAD_PHOTOS_ENDPOINT = "/management-inspections/uploadphotos"
UPLOAD_PHOTOS_STATUS_ENDPOINT = "/management-inspections/uploadphotos/status"



# OAUTH CREDENTIALS

HDI_CLIENT_ID = os.getenv("HDI_CLIENT_ID")
HDI_CLIENT_SECRET = os.getenv("HDI_CLIENT_SECRET")


USE_HDI_MOCK = True
