"""
config.py

Archivo de configuración central del scraper.
Aquí están TODOS los valores que cambian de una página a otra.
Para adaptar el scraper a otra web, este es el ÚNICO archivo que necesitas tocar.

"""


##########################################################
#                   CONFIGURACIÓN GENERAL                #
##########################################################

# Ruta al ejecutable de Camoufox
CAMOUFOX_PATH = r"C:\Users\migue\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\Local\camoufox\camoufox\Cache\camoufox.exe"

# Archivo donde se guardan las cookies de sesión
COOKIES_FILE = "cookies.json"

# Archivo CSV de salida
CSV_FILE = "resultados.csv"

# Encabezados del CSV (deben coincidir con las claves que devuelve el scraper)
CSV_HEADERS = ["Título", "Fecha", "URL_PDF"]

# Página desde la que empezar (0 = desde el principio)
PAGINA_INICIO = 0

# Límite de páginas a scrapear (None = sin límite, scrapeea todo)
MAX_PAGINAS = None


##########################################################
#                       URLs                             #
##########################################################

# URL base del sitio (se usa para construir URLs absolutas)
BASE_URL = "https://www.wri.org"

# URL del listado paginado. Usa {} donde va el número de página
URL_LISTADO = "https://www.wri.org/resources/type/research-65?query=&sort_by=created&page={}"


##########################################################
#                     LOCALIZADORES                      #
##########################################################

# -- Listado --

# Contenedor de cada resultado en el listado
ELEMENT_SCRAP_LOCATOR = "div.ds-1col.clearfix.search-results-container.margin-bottom-sm"

# Título del resultado (también contiene el href a la página de detalle)
TITLE_LOCATOR = "h3.h3 a"

# Fecha del resultado
DATE_LOCATOR = "span.post-date"

# -- Página de detalle --

# Tipo A: botón que abre el modal con formulario de descarga
DOWNLOAD_LOCATOR = "a.webform-dialog.button"

# Tipo B: enlace directo al PDF sin modal
DIRECT_PDF_LOCATOR = "a.button.offsite[href*='.pdf']"

# Botón para saltar el login dentro del modal
SKIP_LOGIN_LOCATOR = "a#skip-registration"

# Enlace al PDF que aparece tras saltar el login
PDF_LOCATOR = "a.button.small.download.document-inline[href*='.pdf']"