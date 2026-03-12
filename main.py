
"""
        Pruebas que hice para evitar el anti-bot
        1- Probar con el perfil de Playright en el navegador 
        2- Probar con el perfil prestablecido diferente al de Playright
        3- Probar con la libreria de Camoufox 
        ? Probar a pedir a la API que me de la  informacion directamente
    


"""
# Importamos la libreria de CAMOUFOX 
from camoufox.sync_api import Camoufox

# Importamos la libreria de json
import json

# Importamos la libreria de os
import os


##########################################################
#                     CONSTANTES                         #
##########################################################

# Url base que vamos a usar para ir a la pagina en detalle de cada elemento
BASE_URL = "https://www.wri.org"

# Url donde vamos a empezar a realizar el scraping
URL_TO_SCRAP  = "https://www.wri.org/resources/type/research-65?query=&sort_by=created&page={}"

# Encabezados de las columnas de nuestro futuro archivo CSV
CSV_HEADERS = ["Título", "Fecha", "URL_PDF"]

# Constante donde vamos a guardar las cookies
COOKIES_FILE = "cookies.json"

######################## LOCALIZADORES ###################

# Localizador padre que engloba todos los elementos que queremos scrapear
FATHER_LOCATOR = "div.ds-1col.clearfix.search-results-container.margin-bottom-sm"

# Localizador de la etiqueta donde se va a encontrar el TITULO
TITLE_LOCATOR = "h3.h3 a"

# Localizador de la etiqueta donde vamos a encontrar la FECHA
DATE_LOCATOR = "span.post-date"

# Localizazdor de la etiqueta donde vamos a encontrar la URL_PDF
PDF_LOCATOR = "a.button.small.download.document-inline"

# Localizador del boton Download
DOWNLOAD_LOCATOR = "a.webform-dialog.button"

# Localizador del botón "Continuar sin loggearse"
SKIP_LOGIN_LOCATOR = "a#skip-registration"

CAMOUFOX_PATH = r"C:\Users\migue\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\Local\camoufox\camoufox\Cache\camoufox.exe"

##########################################################
#                     FUNCIONES                          #
##########################################################

# Definimos la funcion que va a GUARDAR COOKIES cuando pasemos el captcha mannualmente
def guardar_cookies(browser):

    """Abre el navegador , espera a que pases el captcha manualmente y guarda la cookies """
    page = browser.new_page()
    page.goto(URL_TO_SCRAP.format(0), wait_until="domcontentloaded")

    print("⚠️  Pasa el captcha manualmente en el navegador...")
    print("⚠️  Cuando la página haya cargado completamente pulsa ENTER aquí.")
    input()

    # Extraemos las COOKIES de la sesion actual 
    cookies = page.context.cookies()

    # Creamos el CONTEXT MANAGER y guardamos las COOKIES en un JSON
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies,f)

    print("✅ Cookies guardadas correctamente.")
    return page


# Definimos la funcion que cargara las COOKIES para que no nos vuelva a pedir el captcha en futuras ocasiones
def cargar_cookies(browser):

    """Carga las cookies guardadas """
    with open(COOKIES_FILE,"r") as f:
        
        # Guardamos la COOKIES deserializa en una lista de Python.
        cookies = json.load(f)

    # Abrimos una nueva pagina een el navegador 
    page = browser.new_page()

    ######## IMPORTANTE CARGAR LAS COOKIES ANTES DE NAVEGAR ######
    # Injectamos las COOKIES en el contexto del navegador 
    page.context.add_cookies(cookies)

    # Esperamos 2 segundos para aseguurar que la s COOKIES se han cargado correctamente
    page.wait_for_timeout(2000)

    # Navegamos a la pagina que queremos hacer el Scraping 
    page.goto(URL_TO_SCRAP.format(0), wait_until="domcontentloaded")

    # Pausa para que la pagina le de tiempo a renderizarse
    page.wait_for_timeout(3000)

    return page

# Definimos la funcion que va a recorrer todos los elementos de la pagina y recoger los valores de TITULO , FECHA , URL_DETALLE
def scrapear_listado(page):

    # Obtenemos todos los elementos de la pagina actual como una lista
    elementos = page.locator(FATHER_LOCATOR).all()

    # Creamos un variable para guardar los resultados
    resultados = []

    # Iniciamos un bucle para reecorrer todos los elementos
    for elemento in elementos:

        # Extraemos el TITULO del elemento 
        titulo = elemento.locator(TITLE_LOCATOR).text_content().strip()

        # Extraemos la FECHA del elemento 
        fecha = elemento.locator(DATE_LOCATOR).text_content().strip()

        # Extraemos la URL de detalle y la completamos con la BASE_URL
        url_detalle = BASE_URL + elemento.locator(TITLE_LOCATOR).get_attribute("href")

        # Guardamos los datos en un diccionario y lo agregamos a la lista
        resultados.append({
            "titulo": titulo,
            "fecha": fecha,
            "url_detalle": url_detalle
        })

    return resultados

# Definimos la funcion que va a ir a cada pagina unitaria del elemento y guardara el href del PDF para luego guardarlo
def scrapear_detalle(page, url_detalle):

    """Navega a la página de detalle, hace click en Download y extrae la URL del PDF."""

    # Navegamos a la pagina de detalle del elemento
    page.goto(url_detalle, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # Hacemos click en el boton de DOWNLOAD
    page.locator(DOWNLOAD_LOCATOR).click()
    page.wait_for_timeout(2000)

    # Hacemos click en "No thanks. Proceed to download." para saltar el login
    page.locator(SKIP_LOGIN_LOCATOR).click()

    # Extraemos la URL del PDF
    url_pdf = page.locator(PDF_LOCATOR).wait_for(state="visible")
    page.wait_for_timeout(3000)

    url_pdf = page.locator(PDF_LOCATOR).get_attribute("href")

    return url_pdf


# Definimos la funcion que va encargarse de la paginacion 


# Declaramos la funcion principal de nuestro script
def main():

    # Declaramos el Context Manager (with)
    with Camoufox(headless=False, executable_path=CAMOUFOX_PATH) as browser:

        # Si no hay COOKIES guardadas las generamos manualmente
        if not os.path.exists(COOKIES_FILE):
            
            page = guardar_cookies(browser) 

        else:

            page = cargar_cookies(browser)
  
        # Eperamos a que cargue los elementos que necesitamos para obtener los datos
        page.locator(FATHER_LOCATOR).first.wait_for(state="visible")

         # Probamos scrapear_detalle y mostramos los resultados
        url_pdf = scrapear_detalle(page,"https://www.wri.org/research/exploring-productivity-and-climate-change-mitigation-potential-transitions-pasture")

        print(f"URL PDF: {url_pdf}")

        # Pagina cargada correctamente
        print("Página cargada correctamente")           
        
# Ejecutamos la funcion main() al ejecutar este archivo
if __name__ == "__main__":

    main()
