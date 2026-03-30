# victoria.py
import pygame
import sys
import math
from config import ANCHO, ALTO, FUENTE_PATH

COLOR_OVERLAY   = (0, 0, 0, 180)
COLOR_TITULO    = (255, 220, 50)
COLOR_SUBTITULO = (150, 220, 100)
COLOR_TEXTO     = (220, 255, 220)
COLOR_BTN       = (30,  80,  30)
COLOR_BTN_HOVER = (50, 130,  50)
COLOR_BTN_BORDE = (80, 180,  80)


class Boton:
    def __init__(self, x, y, ancho, alto, texto):
        self.rect  = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.hover = False

    def dibujar(self, ventana, fuente):
        color = COLOR_BTN_HOVER if self.hover else COLOR_BTN
        pygame.draw.rect(ventana, color, self.rect, border_radius=12)
        pygame.draw.rect(ventana, COLOR_BTN_BORDE, self.rect, 2, border_radius=12)
        surf = fuente.render(self.texto, True, COLOR_TEXTO)
        ventana.blit(surf, surf.get_rect(center=self.rect.center))

    def actualizar(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def fue_clickeado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


def dibujar_estrella(ventana, cx, cy, r_ext, r_int, color):
    puntos = []
    for i in range(10):
        angulo = math.pi / 5 * i - math.pi / 2
        r      = r_ext if i % 2 == 0 else r_int
        puntos.append((
            cx + r * math.cos(angulo),
            cy + r * math.sin(angulo),
        ))
    pygame.draw.polygon(ventana, color, puntos)


class PantallaVictoria:
    def __init__(self, ventana, fondo_surf, vidas_restantes):
        self.ventana         = ventana
        self.fondo_surf      = fondo_surf
        self.vidas_restantes = vidas_restantes

        self.fuente_titulo  = pygame.font.Font(FUENTE_PATH, 28)
        self.fuente_sub     = pygame.font.Font(FUENTE_PATH, 11)
        self.fuente_botones = pygame.font.Font(FUENTE_PATH, 13)

        bw, bh = 300, 56
        cx = ANCHO // 2 - bw // 2
        self.btn_siguiente = Boton(cx, ALTO // 2 + 40,  bw, bh, "SIGUIENTE NIVEL")
        self.btn_menu      = Boton(cx, ALTO // 2 + 116, bw, bh, "MENU PRINCIPAL")
        self.botones       = [self.btn_siguiente, self.btn_menu]

    def ejecutar(self):
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for boton in self.botones:
                    if boton.fue_clickeado(evento):
                        if boton == self.btn_siguiente:
                            return "siguiente"
                        if boton == self.btn_menu:
                            return "menu"

            self.ventana.blit(self.fondo_surf, (0, 0))

            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill(COLOR_OVERLAY)
            self.ventana.blit(overlay, (0, 0))

            dibujar_estrella(self.ventana, ANCHO // 2 - 220, ALTO // 2 - 110, 30, 13, (255, 200, 0))
            dibujar_estrella(self.ventana, ANCHO // 2,       ALTO // 2 - 140, 38, 16, (255, 220, 0))
            dibujar_estrella(self.ventana, ANCHO // 2 + 220, ALTO // 2 - 110, 30, 13, (255, 200, 0))

            titulo = self.fuente_titulo.render("NIVEL COMPLETADO", True, COLOR_TITULO)
            self.ventana.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 60)))

            sub = self.fuente_sub.render("El sapo llego a la cima del cafe!", True, COLOR_SUBTITULO)
            self.ventana.blit(sub, sub.get_rect(center=(ANCHO // 2, ALTO // 2 + 10)))

            for boton in self.botones:
                boton.actualizar(mouse_pos)
                boton.dibujar(self.ventana, self.fuente_botones)

            pygame.display.flip()
            clock.tick(60)