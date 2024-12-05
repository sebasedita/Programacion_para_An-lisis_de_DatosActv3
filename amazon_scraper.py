from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Configurar opciones de Chrome en modo headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Ejecutar en modo headless para no mostrar la interfaz
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Inicializar el WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL del producto en Amazon
url_producto = "https://www.amazon.com/-/es/EMOPET-Desk-Robot-Companion-personalidad/dp/B0DG8JPL6J"
driver.get(url_producto)

# Esperar hasta que el nombre del producto esté presente en la página
try:
    # Esperar el título del producto
    nombre_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "productTitle"))
    )

    # Obtener el HTML de la página
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")

    # Extraer el nombre del producto
    nombre = soup.find("span", id="productTitle").get_text(strip=True)

    # Extraer el precio del producto
    precio_element = soup.find("span", class_="a-offscreen")
    precio = precio_element.get_text(strip=True) if precio_element else "No disponible"

    # Extraer la descripción breve del producto
    descripcion_element = soup.find("div", id="feature-bullets")
    descripcion = descripcion_element.get_text(strip=True) if descripcion_element else "No disponible"

    # Extraer las calificaciones
    calificaciones_element = soup.find("span", class_="a-icon-alt")
    calificaciones = calificaciones_element.get_text(strip=True) if calificaciones_element else "No disponible"

    # Extraer el vendedor
    vendido_por_element = soup.find("a", id="bylineInfo")
    vendido_por = vendido_por_element.get_text(strip=True) if vendido_por_element else "No disponible"

    # Extraer el fabricante (buscando en detalles del producto)
    detalles_producto = soup.find("div", id="detailBulletsWrapper_feature_div")
    fabricante = "No disponible"
    if detalles_producto:
        for li in detalles_producto.find_all("li"):
            if "Fabricante" in li.get_text(strip=True):
                fabricante = li.get_text(strip=True).replace("Fabricante:", "").strip()
                break

    # Imprimir los datos del producto
    print("Nombre del producto:", nombre)
    print("Precio:", precio)
    print("Descripción:", descripcion)
    print("Calificaciones:", calificaciones)
    print("Vendido por:", vendido_por)
    print("Fabricante:", fabricante)

except Exception as e:
    print("Error al extraer información:", e)

# Cerrar el navegador
driver.quit()
