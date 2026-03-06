
"""
    Plantilla de Web Scrapper con Playwright

    


"""
from playwright.sync_api import sync_playwright

##########################################################
#                     CONSTANTES                         #
##########################################################

# Url donde vamos a empezar a realizar el scraping
URL_TO_SCRAP  = "https://www.wri.org/resources/type/research-65?query=&sort_by=created"
# Encabezados de las columnas de nuestro futuro archivo CSV
CSV_HEADERS = ["Título", "Fecha", "URL_PDF"]

######################## LOCALIZADORES ###################

# Localizador padre que engloba todos los elementos que queremos scrapear
FATHER_LOCATOR = "div.ds-1col.clearfix.search-results-container.margin-bottom-sm"

# Localizador de la etiqueta donde se va a encontrar el TITULO
TITLE_LOCATOR = ""

# Localizador de la etiqueta donde vamos a encontrar la FECHA
DATE_LOCATOR = ""

# Localizazdor de la etiqueta donde vamos a encontrar la URL_PDF
PDF_LOCATOR = ""


# Declaramos la funcion principal de nuestro script
def main():

    # Declaramos el Context Manager (with)
    with sync_playwright() as p:

        # Llamamos a (p) que es el controlador principal de Playwright para lanzar el navegador
        context = p.chromium.launch_persistent_context(user_data_dir="perfil",headless=False,channel= "chrome",user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36") # True  = navegador invisible/ False = visible

        # Creacion de una nueva pagina
        page = context.new_page()

        # Vamos a la web donde haremos el scraping
        page.goto(URL_TO_SCRAP)

        # Esperamos a que la red este inactiva y no haya mas peticiones
        page.wait_for_load_state("domcontentloaded")

        # Eperamos a que cargue los elementos que necesitamos para obtener los datos
        page.locator(FATHER_LOCATOR).first.wait_for(state="visible")

        # Pagina cargada correctamente
        print("Página cargada correctamente")
        
        # Llamada a la funcion que va a scrapear la informacion

        # Llamada a la funcion que va a guardar los resultados en un CSV


        # Cerramos el navegador tras realizar la tarea 
        context.close()

# Ejecutamos la funcion main() al ejecutar este archivo
if __name__ == "__main__":

    main()