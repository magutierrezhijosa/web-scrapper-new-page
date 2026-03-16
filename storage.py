"""
storage.py

Modulo encargado de guardar los resultados del scraping.
Actualmente guarda en CSV, pero se puede extender facilmente
para guardar JSON , base de datos, etc.

"""

# Importamos csv para escribir el resultado CSV
import csv

# Importamos os para comprobar si el archivo ya existe
import os

# Importamos las constanntes que necesitamos de config.py
from config import CSV_FILE,CSV_HEADERS


##########################################################
#                     FUNCIONES                          #
##########################################################

def guardar_csv(resultados,modo="a"):

    """
    Guarda una lista de resultados en el archivo CSV .
    Por defecto usa modo append ('a') para no sobreescribir datos anteriores.
    Solo escribe el  encabezado si el archivo es nuevo
    
    """

    # Comprobamos si el archivo ya existe para no escribir el encabezado dos veces 
    archivo_existe = os.path.exists(CSV_FILE)

    # Creamos el context manager (with)
    with open(CSV_FILE, modo, newline="", encoding="utf-8") as f:

        # Creamos el escritor para CSV y le agregamos los encabezados
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)

        # Solo escribimos el encabezado si el archivo es nuevo
        if not archivo_existe or modo=="w":

            writer.writeheader()

        