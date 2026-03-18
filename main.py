
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
from cookies import guardar_cookies, cargar_cookies

# Importamos las funciones de scraper.py
from scraper import scrapear_todas_las_paginas

# Importamos las funciones de storage.py
from storage import borrar_csv