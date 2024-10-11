from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os
import shutil
import time
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/ejecutar")
def ejecutar_rpa():
    try:
        logger.info("Iniciando Firefox para ejecutar el script")

        # Definir la carpeta de descargas
        download_dir = os.path.abspath("./downloads")
        os.makedirs(download_dir, exist_ok=True)

        # Configurar opciones de Firefox para deshabilitar la verificación de certificados
        options = Options()
        options.set_preference("browser.download.folderList", 2)  # Usar una carpeta específica
        options.set_preference("browser.download.dir", download_dir)  # Carpeta de destino
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/msword")  # Tipos de archivos a descargar automáticamente
        options.set_preference("pdfjs.disabled", True)  # Desactivar visor de PDF en Firefox
        options.set_preference("network.proxy.type", 0)  # Desactivar proxy
        options.set_preference("security.ssl.enable_ocsp_stapling", False)  # Desactivar OCSP Stapling
        options.set_preference("security.cert_pinning.enforcement_level", 0)  # Desactivar pinning de certificados
        options.set_preference("webdriver_accept_untrusted_certs", True)
        options.set_preference("webdriver_assume_untrusted_issuer", False)

        # Iniciar Firefox
        driver = webdriver.Firefox(options=options)

        # Crear la carpeta 'screenshots' si no existe
        screenshots_folder = './screenshots'
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)

        # Cargar la página principal
        driver.get("https://www.supertransporte.gov.co/index.php/vigia/")

        # Esperar un tiempo para que la página cargue completamente
        time.sleep(5)

        # Tomar captura de pantalla después de cargar la página
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(screenshots_folder, f"screenshot_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Captura de pantalla guardada en: {screenshot_path}")

        # Usar el XPath proporcionado para encontrar el enlace y hacer clic en él
        certificado_link = driver.find_element(By.XPATH, '//*[@id="post-6544"]/div/div[4]/div/div[2]/div/div[2]/p/span[2]/a')
        certificado_link.click()

        # Cambiar al nuevo tab/ventana donde se abrió el PDF
        driver.switch_to.window(driver.window_handles[-1])

        # Esperar unos segundos para que el archivo se descargue
        time.sleep(10)

        # Verificar si el archivo fue descargado
        downloaded_files = os.listdir(download_dir)
        if downloaded_files:
            logger.info(f"Archivo descargado: {downloaded_files[0]}")
            downloaded_file = downloaded_files[0]
        else:
            logger.error("No se encontró ningún archivo descargado")
            downloaded_file = None

        # Cerrar el navegador
        driver.quit()
        
        # if os.path.exists(f"./downloads/{downloaded_file}"):
        #     os.remove(f"./downloads/{downloaded_file}")
        #     return {"message": "existe"}
        # else:
        #     return {"message": "no existe"}

        return {"message": "Script ejecutado correctamente", "archivo_descargado": downloaded_file}
    
    except Exception as e:
        logger.error(f"Error al ejecutar el script: {str(e)}")
        return {"message": f"Error al ejecutar el script: {str(e)}"}
