"""
storage.py

Modulo encargado dee guardar los resultados del scraping.
Actualmente guarda en CSV, pero se puede extender facilmente
para guardar JSON , base de datos, etc.

"""

# Importamos csv para escribir el resultado CSV
import csv

# Importamos os para comprobar si el archivo ya existe
import os

# Importamos las constanntes que necesitamos de config.py
from config import CSV_FILE,CSV_HEADERS