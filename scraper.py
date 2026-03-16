
# Importamos las CONSTANTES quue vamos a usar del config.py
from config import ELEMENT_SCRAP_LOCATOR , TITLE_LOCATOR , DATE_LOCATOR , URL_LISTADO, BASE_URL

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
        url_detalle = BASE_URL + elemento.locator(URL_LISTADO).get_attribute("href")

        # Guardamos los datos en un diccionario y lo agregamos a la lista
        resultados.append({

            "titulo":titulo,
            "fecha": fecha,
            "url_detalle": url_detalle

        })

        return resultados

