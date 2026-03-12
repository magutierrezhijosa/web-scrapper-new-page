
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

# Importamos la libreria de csv
import csv

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

# Nombre del archivo CSV donde guardaremos los resultados
CSV_FILE = "resultados.csv"

# Ruta  para poder ejecutar correctamente el .exe de CAMOUFOX
CAMOUFOX_PATH = r"C:\Users\migue\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\Local\camoufox\camoufox\Cache\camoufox.exe"

######################## LOCALIZADORES ###################

# Localizador padre que engloba todos los elementos que queremos scrapear
FATHER_LOCATOR = "div.ds-1col.clearfix.search-results-container.margin-bottom-sm"

# Localizador de la etiqueta donde se va a encontrar el TITULO
TITLE_LOCATOR = "h3.h3 a"

# Localizador de la etiqueta donde vamos a encontrar la FECHA
DATE_LOCATOR = "span.post-date"

# Localizazdor de la etiqueta donde vamos a encontrar la URL_PDF
PDF_LOCATOR = "a.button.small.download.document-inline[href*='.pdf']"

# Localizador Tipo A del boton Download
DOWNLOAD_LOCATOR = "a.webform-dialog.button"

# Localizador Tipo B - solo enlaces directos a PDF
DIRECT_PDF_LOCATOR = "a.button.offsite[href*='.pdf']"

# Localizador del botón "Continuar sin loggearse"
SKIP_LOGIN_LOCATOR = "a#skip-registration"



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

    # Intentamos navegar hasta 3 veces por si hay timeout
    for intento in range(3):
        try:
            page.goto(url_detalle, wait_until="domcontentloaded", timeout=60000)
            break
        except:
            print(f"⚠️  Timeout navegando a {url_detalle}, intento {intento + 1}/3")
            if intento == 2:
                return None
            page.wait_for_timeout(3000)
    
    page.wait_for_timeout(2000)

    # Comprobamos si es de tipo B Directo el boton DOWNLOAD
    if page.locator(DIRECT_PDF_LOCATOR).count() > 0:
        url_pdf = page.locator(DIRECT_PDF_LOCATOR).first.get_attribute("href")
        return url_pdf
    
    # Si no , es tipo A (modal con formulario)
    # Comprobamos que hay boton de DOWNLOAD
    if page.locator(DOWNLOAD_LOCATOR).count() == 0:
        print(f"⚠️  No se encontró botón Download en: {url_detalle}")
        return None
    
    # Hacemos click en el boton de DOWNLOAD
    page.locator(DOWNLOAD_LOCATOR).click()
    page.wait_for_timeout(2000)

    # Comprobamos si hay Boton de SKIP_LOGIN
    if page.locator(SKIP_LOGIN_LOCATOR).count() == 0:
        print(f"⚠️  No se encontró botón Skip en: {url_detalle}")
        return None
    
    # Hacemos click en "No thanks. Proceed to download." para saltar el login
    page.locator(SKIP_LOGIN_LOCATOR).click()

    # Comprobamos que haya URL del PDF antes de acceder a la data
    if page.locator(PDF_LOCATOR).count() == 0:
        print(f"⚠️  No se encontró PDF en: {url_detalle}")
        return None

    # Extraemos la URL del PDF
    page.locator(PDF_LOCATOR).first.wait_for(state="visible")
    page.wait_for_timeout(3000)

    url_pdf = page.locator(PDF_LOCATOR).first.get_attribute("href")

    return url_pdf


# Definimos la funcion que va encargarse de la paginacion 
def scrapear_todas_las_paginas(page):

    """Recorre todas las páginas del listado y extrae todos los datos."""

    # Declaramos la variable donde guardaremos todos los resultados de todas la paginas 
    todos_los_resultados = []

    # Declaramos la variable qque sigue el conteo de la paginacion
    numero_pagina = 0

    # Cambia esto en scrapear_todas_las_paginas para limitar las páginas en pruebas
    MAX_PAGINAS = None  # Cambia a None para scrappear todo

    # Creamos un buclee While que mientras encuentra elemento los scrapea sino para y al final de cada iteracion incrementa el numero de pagina
    while True:

        # Limite de paginas para pruebas
        if MAX_PAGINAS and numero_pagina >= MAX_PAGINAS:
            print(f"✅ Límite de {MAX_PAGINAS} páginas alcanzado.")
            break

        # Mostramos en consola la pagina por la que vamos 
        print(f"📄 Scrapeando página {numero_pagina}...")

        # Navegamos a la pagina actual del listado 
        page.goto(URL_TO_SCRAP.format(numero_pagina),wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # Comprobamos si hay elementos en la pagina 
        # Si no hay elemento es que hemos llegado al final 
        if page.locator(FATHER_LOCATOR).count() == 0:

            print("✅ No hay más páginas.")
            break

        # Scrapeamos lso resultados de la pagina 
        resultados_pagina = scrapear_listado(page)

        # Para cada elemento entramos en detalle y extraemos el PDF
        for resultado in resultados_pagina:

            # Recogemos la URL del PDF en una una variable 
            url_pdf = scrapear_detalle(page,resultado["url_detalle"])

            # Agregamos la URL del PDF al resultado
            resultado["url_pdf"] = url_pdf 

            print(f"✅ Scrapeado: {resultado['titulo'][:50]}...")   

            # Añadimos el resultado completo a la lista total
            todos_los_resultados.append(resultado)

        numero_pagina += 1

    return todos_los_resultados

# Definimos la funcion que va a encargarse de guardar los datos en un CSV
def guardar_csv(resultados):

    # Abrimos el archivo CSV /en modo escritura "w"/newline="" (evita  que se agregen lineas en blanco/con utf-8 para aceptar tildes y n)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:

        # Creamos el escritos CSV
        writer = csv.DictWriter(f,fieldnames=CSV_HEADERS)

        # Escribimos la fila del encabezado
        writer.writeheader()

        # Recorremos los resultados y escribimos cada fila
        for resultado in resultados:
            writer.writerow({
                "Título": resultado["titulo"],
                "Fecha": resultado["fecha"],
                "URL_PDF":resultado["url_pdf"]

            })

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

        # Probamos con las 2 primeras páginas
        resultados = scrapear_todas_las_paginas(page)

        # Guardamos los resultados en CSV
        guardar_csv(resultados)

        # Pagina cargada correctamente
        print(f"✅ Script finalizado. {len(resultados)} elementos guardados en {CSV_FILE}")       
        
# Ejecutamos la funcion main() al ejecutar este archivo
if __name__ == "__main__":

    main()
