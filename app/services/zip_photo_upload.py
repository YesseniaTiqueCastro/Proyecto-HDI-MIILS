import requests
import os


def subir_zip_fotos_s3(
    upload_url: str,
    zip_path: str
):
    """
    Sube el archivo ZIP de fotos a S3 usando la URL presigned (PUT)
    """

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"No se encontró el archivo ZIP: {zip_path}")

    headers = {
        "Content-Type": "application/zip"
    }

    with open(zip_path, "rb") as zip_file:
        response = requests.put(
            upload_url,
            data=zip_file,
            headers=headers
        )

    return response.status_code, response.text
