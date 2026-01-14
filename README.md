# Consumo API proyecto HDI – Gestión de Inspecciones

# Descripción
Proyecto realizado en Python para el consumo de la API de HDI Seguros relacionada con la gestión de inspecciones de vehiculos.

# Arquitectura
- Python V 3.14.2
- Requests
- Autenticación OAuth 2.0 Client Credentials
- Estructura modular por servicios

# Flujo implementado
1. Autenticación (token)
2. Health Check (estado de los servicios)
3. Consulta de inspección (pendiente por insumos de negocio)
4. Gestión de inspección (pendiente por insumos de negocio)
5. Cargue de fotos:
   - Generación de URL prefirmada
   - PUT del ZIP a S3
   - Consulta de estado del cargue

# Estado actual
- El flujo de cargue de fotos se encuentra completamente funcional.
- Los endpoints de consulta y gestión dependen de datos funcionales provistos por HDI (inspecciones, placas y catálogo de calificaciones).

# Estructura del proyecto
(app/config, core, models,services,utils,resources, requirements)

# Cómo ejecutar
1. Crear entorno virtual
2. Instalar dependencias
3. Ejecutar main.py

# Endpoints y URL ambiente de pruebas

HEALTH_ENDPOINT = "/vehicle-services/health"
TOKEN_ENDPOINT = "/vehicle-services/token"
CONSULTA_INSPECCION_ENDPOINT = "/vehicle-services/crearConsultarInspMIILS"
GESTION_INSPECCION_ENDPOINT = "/management-inspections/gestionarInspMIILS"
"HDI_BASE_URL",
    "https://nonprod-apis-auto.hdiseguros.com.co"