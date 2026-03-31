# parallax.py
import pygame
from config import ANCHO, ALTO


class Parallax:
    def __init__(self):
        self.capas = []

    def cargar_capas(self, capas_config):
        """Carga las capas del fondo según la configuración del nivel."""
        self.capas = []
        for ruta, velocidad in capas_config:
            try:
                img = pygame.image.load(ruta).convert_alpha()
                img = pygame.transform.scale(img, (ANCHO, ALTO))
                self.capas.append((img, velocidad))
            except Exception as e:
                print(f"No se pudo cargar capa: {ruta} — {e}")

    def dibujar(self, ventana, offset_x, offset_y):
        for img, velocidad in self.capas:
            dx = int(offset_x * velocidad) % ANCHO
            dy = int(offset_y * velocidad * 0.3) % ALTO
            ventana.blit(img, (-dx,         -dy))
            ventana.blit(img, (-dx + ANCHO,  -dy))
            ventana.blit(img, (-dx - ANCHO,  -dy))