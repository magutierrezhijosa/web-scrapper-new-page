
"""
cookies.py

Módulo encargado de gestionar las cookies de sesión.
Permite guardarlas manualmente (pasando el captcha) y cargarlas en futuras ejecuciones.
"""

# Importamos json para serializar/deserializar las cookies
import json

# Importamos os para comprobar si el archivo de cookies existe
import os

# Importamos las constantes que necesitamos de config.py
from config import COOKIES_FILE, URL_LISTADO , ELEMENT_SCRAP_LOCATOR


##########################################################
#                     FUNCIONES                          #
##########################################################

def guardar_cookies(browser):
    """
    1.-Abre el navegador, 
    2.-Espera a que el usuario pase el captcha 
    manualmente 
    3.Guarda las cookies en un archivo JSON.

    """
    page = browser.new_page()
    page.goto(URL_LISTADO.format(0), wait_until="domcontentloaded")

    print("⚠️  Pasa el captcha manualmente en el navegador...")
    print("⚠️  Cuando la página haya cargado completamente pulsa ENTER aquí.")
    input()

    # Extraemos las cookies de la sesión actual
    cookies = page.context.cookies()

    # Guardamos las cookies serializadas en un JSON
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f)

    print("✅ Cookies guardadas correctamente.")
    return page


def cargar_cookies(browser):
    """
    Carga las cookies guardadas e inyecta en el contexto del navegador
    para evitar volver a pasar el captcha.
    """
    with open(COOKIES_FILE, "r") as f:
        cookies = json.load(f)

    page = browser.new_page()

     ######## IMPORTANTE CARGAR LAS COOKIES ANTES DE NAVEGAR ######
    # Injectamos las COOKIES en el contexto del navegador 
    page.context.add_cookies(cookies)

    # Esperamos 2 segundos para aseguurar que la s COOKIES se han cargado correctamente
    page.wait_for_timeout(2000)

    # Navegamos a la pagina que queremos hacer el Scraping 
    page.goto(URL_LISTADO.format(0), wait_until="domcontentloaded")
    
    # Pausa para que la pagina le de tiempo a renderizarse
    page.wait_for_timeout(3000)

     # Comprobamos si las cookies siguen siendo válidas
    try:
        page.locator(ELEMENT_SCRAP_LOCATOR ).first.wait_for(state="visible", timeout=5000)
        print("✅ Cookies cargadas y válidas.")
        return page
    

    except:
        # Las cookies han caducado, las borramos y pedimos nuevas
        print("⚠️  Las cookies han caducado, vuelve a pasar el captcha.")
        os.remove(COOKIES_FILE)
        return guardar_cookies(browser)


def cookies_existen():
    """
    Comprueba si ya existe un archivo de cookies guardado.
    Devuelve True si existe, False si no.
    """
    return os.path.exists(COOKIES_FILE)