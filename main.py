from app.services.health import health_check
from app.services.consultation import consultar_inspeccion
from app.services.inspection_management import gestionar_inspeccion
from app.services.photo_upload import generar_presigned_url_fotos
from app.services.photo_upload_status import consultar_estado_cargue_fotos


if __name__ == "__main__":
    print("Consumo HDI")

    ID_INSPECCION = "12274"
    USUARIO = "WS_COLSERAUTO"

    print("\n--- Endpoint Health Check ---")
    health_status, _ = health_check()
    print("Health Status:", health_status)

    print("\n--- Endpoint Consulta de Inspección ---")
    consulta_status, consulta_response = consultar_inspeccion(placa="DXL632")
    print("Consulta Status:", consulta_status)
    print("Consulta Response:", consulta_response)
 

    print("\n--- Endpoint Gestión de Inspección ---")
    gestion_status, gestion_response = gestionar_inspeccion(
        id_inspeccion=ID_INSPECCION,
        usuario=USUARIO,
        fecha_hora_inspeccion="2026-01-13T10:30:00Z",
        fecha_hora_salida_inspeccion="2026-01-13T11:00:00Z"
    )
    print("Gestión Status:", gestion_status)
    print("Gestión Response:", gestion_response)

    print("\n--- Endpoint Generar Presigned URL Fotos ---")
    upload_status, upload_response = generar_presigned_url_fotos(
        id_inspeccion=ID_INSPECCION,
        usuario=USUARIO
    )
    print("Upload Status:", upload_status)
    print("Upload Response:", upload_response)

    print("\n--- Endpoint Estado Cargue de Fotos ---")
    status_code, status_response = consultar_estado_cargue_fotos(
        id_inspeccion=ID_INSPECCION,
        usuario=USUARIO
    )
    print("Status Fotos:", status_code)
    print("Response Fotos:", status_response)
