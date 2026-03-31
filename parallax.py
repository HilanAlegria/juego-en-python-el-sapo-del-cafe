# parallax.py
import pygame
from config import ANCHO, ALTO


# parallax.py
class Parallax:
    def __init__(self):
        self.capas = []

    def cargar_capas(self, capas_config):
        self.capas = []

    def dibujar(self, ventana, offset_x, offset_y):
        pass