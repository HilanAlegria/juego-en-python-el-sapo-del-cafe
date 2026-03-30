# hud.py
import pygame
from config import ANCHO

COLOR_HUD_FONDO = (0, 0, 0, 120)
COLOR_CORAZON   = (220, 50,  50)
COLOR_VACIO     = (60,  60,  60)
COLOR_LABEL     = (180, 255, 180)

FUENTE = "fuentes/PressStart2P-Regular.ttf"


def dibujar_corazon(ventana, cx, cy, tamanio, color):
    r = tamanio // 2
    pygame.draw.circle(ventana, color, (cx - r // 2, cy - r // 3), r // 2 + 1)
    pygame.draw.circle(ventana, color, (cx + r // 2, cy - r // 3), r // 2 + 1)
    puntos = [
        (cx - r, cy - r // 3),
        (cx + r, cy - r // 3),
        (cx,     cy + r),
    ]
    pygame.draw.polygon(ventana, color, puntos)


class HUD:
    def __init__(self, vidas_max=3):
        self.vidas_max    = vidas_max
        self.fuente_label = pygame.font.Font(FUENTE, 11)
        self.tamanio_ico  = 22

    def dibujar(self, ventana, vidas):
        barra = pygame.Surface((ANCHO, 48), pygame.SRCALPHA)
        barra.fill(COLOR_HUD_FONDO)
        ventana.blit(barra, (0, 0))

        label = self.fuente_label.render("VIDAS", True, COLOR_LABEL)
        ventana.blit(label, (16, 14))

        for i in range(self.vidas_max):
            color = COLOR_CORAZON if i < vidas else COLOR_VACIO
            cx    = 90 + i * (self.tamanio_ico + 10)
            cy    = 24
            dibujar_corazon(ventana, cx, cy, self.tamanio_ico, color)