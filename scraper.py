
# Importamos las CONSTANTES quue vamos a usar del config.py
from config import ELEMENT_SCRAP_LOCATOR , TITLE_LOCATOR , DATE_LOCATOR , URL_LISTADO, BASE_URL ,  DIRECT_PDF_LOCATOR , DOWNLOAD_LOCATOR , SKIP_LOGIN_LOCATOR , PDF_LOCATOR , MAX_PAGINAS , PAGINA_INICIO

from storage import guardar_csv

"""
    scraper.py

    Modulo encargado de sacar la informacion de la lista de elementos 
    Ademas tenndra otra funcion que recogera la informacion en detalle de cada elemento 

"""

# Declaramos la funcion para haceer el scrap a el conjunnto de elementos
def scrapear_listado(page):

    # Obtenemos todos los elementos de la pagina actual comm una lista
    elementos = page.locator(ELEMENT_SCRAP_LOCATOR).all()

    # Creamos una variable para guardar los resultados
    resultados = []

    # Recorremos los elementos en un bucle para recoger la data de cada uno de ellos
    for elemento in elementos:

        # Extraemos el TITULO del elemento
        titulo = elemento.locator(TITLE_LOCATOR).text_content().strip()

        # Extraemos la FECHA del elemento
        fecha = elemento.locator(DATE_LOCATOR).text_content().strip()

        # Extraemos la URL de detalle y la completamos con la URL_BASE
        url_detalle = BASE_URL + elemento.locator(TITLE_LOCATOR).get_attribute("href")

        # Guardamos los datos en un diccionario y lo agregamos a la lista
        resultados.append({

            "titulo":titulo,
            "fecha": fecha,
            "url_detalle": url_detalle

        })

    return resultados

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
    
    download_button = page.locator(DOWNLOAD_LOCATOR).first
    download_button.wait_for(state="visible")
    download_button.click(no_wait_after=True,timeout=60000)
    page.wait_for_timeout(2000)

    # Comprobamos si hay Boton de SKIP_LOGIN
    if page.locator(SKIP_LOGIN_LOCATOR).count() == 0:
        print(f"⚠️  No se encontró botón Skip en: {url_detalle}")
        return None
    
    # Hacemos click en "No thanks. Proceed to download." para saltar el login
    skip_button = page.locator(SKIP_LOGIN_LOCATOR).first

    if skip_button.count() == 0:
        print(f"⚠️  No se encontró botón Skip en: {url_detalle}")
        return None

    skip_button.wait_for(state="visible")
    try:
        skip_button.click(timeout=60000, force=True)
    except:
        print(f"⚠️  No se pudo hacer click en skip en: {url_detalle}")
        return None
    
    # Esperamos más tiempo a que el modal se cierre y aparezca el PDF
    page.wait_for_timeout(5000)  # ← sube de 3000 a 5000

    # Si el PDF no aparece, continuamos sin romper el script
    try:
        page.locator(PDF_LOCATOR).first.wait_for(state="visible", timeout=60000)
        url_pdf = page.locator(PDF_LOCATOR).first.get_attribute("href")

        return url_pdf
    
    except:

        print(f"⚠️  PDF no apareció tras skip en: {url_detalle}")
       
        return None
    
# Definimos la funcion que va encargarse de la paginacion 
def scrapear_todas_las_paginas(page):

    """Recorre todas las páginas del listado y extrae todos los datos."""

    # Declaramos la variable donde guardaremos todos los resultados de todas la paginas 
    todos_los_resultados = []

    # Declaramos la variable qque sigue el conteo de la paginacion
    numero_pagina = PAGINA_INICIO


    # Creamos un buclee While que mientras encuentra elemento los scrapea sino para y al final de cada iteracion incrementa el numero de pagina
    while True:

        # Limite de paginas para pruebas
        if MAX_PAGINAS and numero_pagina >= MAX_PAGINAS:
            print(f"✅ Límite de {MAX_PAGINAS} páginas alcanzado.")
            break

        # Mostramos en consola la pagina por la que vamos 
        print(f"📄 Scrapeando página {numero_pagina}...")

        # Navegamos a la pagina actual del listado 
        page.goto(URL_LISTADO.format(numero_pagina),wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # Comprobamos si hay elementos en la pagina 
        # Si no hay elemento es que hemos llegado al final 
        if page.locator(ELEMENT_SCRAP_LOCATOR).count() == 0:

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

        
        # Guardamos los resultados de esta página inmediatamente
        guardar_csv(resultados_pagina)
        print(f"💾 Página {numero_pagina} guardada en CSV ({len(resultados_pagina)} elementos)")

        numero_pagina += 1

    return todos_los_resultados
  