
"""
    Plantilla de Web Scrapper con Playwright

    


"""
from camoufox.sync_api import Camoufox

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

CAMOUFOX_PATH = r"C:\Users\migue\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\Local\camoufox\camoufox\Cache\camoufox.exe"


# Declaramos la funcion principal de nuestro script
def main():

    # Declaramos el Context Manager (with)
    with Camoufox(headless=False, executable_path=CAMOUFOX_PATH) as browser:

        # Creacion de una nueva pagina
        page = browser.new_page()

        # Vamos a la web donde haremos el scraping
        page.goto(URL_TO_SCRAP)

        # Esperamos a que la red este inactiva y no haya mas peticiones
        page.wait_for_load_state("domcontentloaded")

        # Eperamos a que cargue los elementos que necesitamos para obtener los datos
        page.locator(FATHER_LOCATOR).first.wait_for(state="visible")

        # Pagina cargada correctamente
        print("Página cargada correctamente")
            
        
# Ejecutamos la funcion main() al ejecutar este archivo
if __name__ == "__main__":

    main()
