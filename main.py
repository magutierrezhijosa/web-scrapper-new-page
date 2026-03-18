
"""
main.py

Punto de entrada principal del scraper.
Aqui dolo esta el flujo de alto nivel - toda la logica esta en los otros modulos

"""


# Importamos Camoufox para abrir el navegador 
from camoufox.sync_api import Camoufox

# Importamos las constantes que necesitamos de config.py
from config import CAMOUFOX_PATH, ELEMENT_SCRAP_LOCATOR

# Importamos las funciones de cookies.py
from cookies import guardar_cookies, cargar_cookies , cookies_existen

# Importamos las funciones de scraper.py
from scraper import scrapear_todas_las_paginas

# Importamos las funciones de storage.py
from storage import borrar_csv

##########################################################
#                     MAIN                              #
##########################################################

def main():

    with Camoufox(headless=False, executable_path=CAMOUFOX_PATH) as browser:

        # Opciona: descomenta esta linea para empezar desde cero borrando el CSV anterior
        # borrar_csv()

        # Gestionamos la cookies - si existen las cargamos, si no las generamos
        if cookies_existen():
            page = cargar_cookies(browser)
        else:
            page = guardar_cookies(browser)

        # Esperamos a que la pagina este lista antes de empezar
        page.locator(ELEMENT_SCRAP_LOCATOR).first.wait_for(state="visible")

        # Lanzamos el scraping 
        resultados = scrapear_todas_las_paginas(page)

        print(f"✅ Script finalizado. {len(resultados)} elementos guardados.")

if __name__ == "__main__":

    main()