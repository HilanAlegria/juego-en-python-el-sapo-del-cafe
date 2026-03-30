# menu.py
import pygame
import sys
from config import ANCHO, ALTO

COLOR_FONDO        = (15, 25, 10)
COLOR_TITULO       = (255, 220, 50)
COLOR_BTN          = (30, 80, 30)
COLOR_BTN_HOVER    = (50, 130, 50)
COLOR_BTN_BORDE    = (80, 180, 80)
COLOR_TEXTO        = (220, 255, 220)
COLOR_TEXTO_OSCURO = (10, 30, 10)
COLOR_SUBTITULO    = (150, 220, 100)

FUENTE = "fuentes/PressStart2P-Regular.ttf"


class Boton:
    def __init__(self, x, y, ancho, alto, texto):
        self.rect  = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.hover = False

    def dibujar(self, ventana, fuente):
        color = COLOR_BTN_HOVER if self.hover else COLOR_BTN
        pygame.draw.rect(ventana, color, self.rect, border_radius=12)
        pygame.draw.rect(ventana, COLOR_BTN_BORDE, self.rect, 2, border_radius=12)
        texto_surf = fuente.render(self.texto, True, COLOR_TEXTO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        ventana.blit(texto_surf, texto_rect)

    def actualizar(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def fue_clickeado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.rect.collidepoint(evento.pos)
        )


class Menu:
    def __init__(self, ventana):
        self.ventana = ventana

        try:
            self.fondo = pygame.image.load("imagenes/fondo Level 1.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
            self.overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            self.overlay.fill((0, 0, 0, 160))
        except:
            self.fondo   = None
            self.overlay = None

        # Fuentes — siempre dentro del __init__, nunca fuera
        self.fuente_titulo    = pygame.font.Font(FUENTE, 36)
        self.fuente_subtitulo = pygame.font.Font(FUENTE, 14)
        self.fuente_botones   = pygame.font.Font(FUENTE, 16)
        self.fuente_small     = pygame.font.Font(FUENTE, 11)

        bw, bh = 300, 60
        cx = ANCHO // 2 - bw // 2
        self.btn_jugar     = Boton(cx, 300, bw, bh, "JUGAR")
        self.btn_sapo      = Boton(cx, 380, bw, bh, "ELEGIR SAPO")
        self.btn_controles = Boton(cx, 460, bw, bh, "CONTROLES")
        self.btn_salir     = Boton(cx, 540, bw, bh, "SALIR")
        self.botones = [self.btn_jugar, self.btn_sapo, self.btn_controles, self.btn_salir]
        self.mostrar_controles = False

    def _dibujar_controles(self):
        panel = pygame.Surface((500, 340), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 200))
        self.ventana.blit(panel, (ANCHO // 2 - 250, ALTO // 2 - 170))

        controles = [
            ("< >",     "Mover izq / der"),
            ("A D",     "Mover izq / der"),
            ("ESPACIO", "Saltar"),
            ("W",       "Saltar"),
            ("ESC",     "Volver al menu"),
        ]

        titulo = self.fuente_subtitulo.render("CONTROLES", True, COLOR_TITULO)
        self.ventana.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 145)))

        for i, (tecla, accion) in enumerate(controles):
            y = ALTO // 2 - 100 + i * 48
            caja = pygame.Rect(ANCHO // 2 - 220, y, 110, 36)
            pygame.draw.rect(self.ventana, COLOR_BTN_HOVER, caja, border_radius=8)
            pygame.draw.rect(self.ventana, COLOR_BTN_BORDE, caja, 2, border_radius=8)
            t = self.fuente_small.render(tecla, True, COLOR_TEXTO)
            self.ventana.blit(t, t.get_rect(center=caja.center))
            d = self.fuente_small.render(accion, True, COLOR_TEXTO)
            self.ventana.blit(d, (ANCHO // 2 - 95, y + 10))

        hint = self.fuente_small.render("ESC o clic para cerrar", True, COLOR_SUBTITULO)
        self.ventana.blit(hint, hint.get_rect(center=(ANCHO // 2, ALTO // 2 + 145)))

    def ejecutar(self):
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.mostrar_controles:
                            self.mostrar_controles = False
                        else:
                            pygame.quit()
                            sys.exit()

                if not self.mostrar_controles:
                    if self.btn_jugar.fue_clickeado(evento):
                        return "jugar"
                    if self.btn_sapo.fue_clickeado(evento):
                        return "elegir_sapo"
                    if self.btn_controles.fue_clickeado(evento):
                        self.mostrar_controles = True
                    if self.btn_salir.fue_clickeado(evento):
                        pygame.quit()
                        sys.exit()
                else:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        self.mostrar_controles = False

            if self.fondo:
                self.ventana.blit(self.fondo, (0, 0))
                self.ventana.blit(self.overlay, (0, 0))
            else:
                self.ventana.fill(COLOR_FONDO)

            titulo = self.fuente_titulo.render("El Sapo del Cafe", True, COLOR_TITULO)
            self.ventana.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 180)))

            sub = self.fuente_subtitulo.render("Sube hasta la cima!", True, COLOR_SUBTITULO)
            self.ventana.blit(sub, sub.get_rect(center=(ANCHO // 2, 260)))

            if not self.mostrar_controles:
                for boton in self.botones:
                    boton.actualizar(mouse_pos)
                    boton.dibujar(self.ventana, self.fuente_botones)
            else:
                self._dibujar_controles()

            pygame.display.flip()
            clock.tick(60)