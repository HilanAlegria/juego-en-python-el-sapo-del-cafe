# menu.py
import pygame
import sys
from config import ANCHO, ALTO, FUENTE_PATH

COLOR_FONDO     = (15, 25, 10)
COLOR_TITULO    = (255, 220, 50)
COLOR_BTN       = (30, 80, 30)
COLOR_BTN_HOVER = (50, 130, 50)
COLOR_BTN_BORDE = (80, 180, 80)
COLOR_TEXTO     = (220, 255, 220)
COLOR_SUBTITULO = (150, 220, 100)

FUENTE = FUENTE_PATH


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


class Menu:
    def __init__(self, ventana, pantalla_completa=False):
        self.ventana           = ventana
        self.pantalla_completa = pantalla_completa

        try:
            self.fondo = pygame.image.load("imagenes/fondo Level 1.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
            self.overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            self.overlay.fill((0, 0, 0, 160))
        except:
            self.fondo   = None
            self.overlay = None

        self.fuente_titulo    = pygame.font.Font(FUENTE, 36)
        self.fuente_subtitulo = pygame.font.Font(FUENTE, 14)
        self.fuente_botones   = pygame.font.Font(FUENTE, 14)
        self.fuente_small     = pygame.font.Font(FUENTE, 10)

        bw, bh = 320, 56
        cx = ANCHO // 2 - bw // 2

        self.btn_jugar      = Boton(cx, 280, bw, bh, "JUGAR")
        self.btn_niveles    = Boton(cx, 356, bw, bh, "NIVELES")
        self.btn_sapo       = Boton(cx, 432, bw, bh, "ELEGIR SAPO")
        self.btn_controles  = Boton(cx, 508, bw, bh, "CONTROLES")
        self.btn_pantalla   = Boton(cx, 584, bw, bh, self._texto_pantalla())
        self.btn_salir      = Boton(cx, 660, bw, bh, "SALIR")

        self.botones = [
            self.btn_jugar, self.btn_niveles, self.btn_sapo,
            self.btn_controles, self.btn_pantalla, self.btn_salir
        ]

        self.mostrar_controles = False

    def _texto_pantalla(self):
        return "MODO VENTANA" if self.pantalla_completa else "PANTALLA COMPLETA"

    def _dibujar_controles(self):
        panel = pygame.Surface((600, 380), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 210))
        self.ventana.blit(panel, (ANCHO // 2 - 300, ALTO // 2 - 190))

        controles = [
            ("< >  /  A D",  "Mover izq / der"),
            ("ESPACIO / W",  "Saltar"),
            ("ESC",          "Volver al menu"),
        ]

        titulo = self.fuente_subtitulo.render("CONTROLES", True, COLOR_TITULO)
        self.ventana.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 155)))

        for i, (tecla, accion) in enumerate(controles):
            y    = ALTO // 2 - 100 + i * 60
            caja = pygame.Rect(ANCHO // 2 - 260, y, 200, 38)
            pygame.draw.rect(self.ventana, COLOR_BTN_HOVER, caja, border_radius=8)
            pygame.draw.rect(self.ventana, COLOR_BTN_BORDE, caja, 2, border_radius=8)
            t = self.fuente_small.render(tecla, True, COLOR_TEXTO)
            self.ventana.blit(t, t.get_rect(center=caja.center))
            d = self.fuente_small.render(accion, True, COLOR_TEXTO)
            self.ventana.blit(d, (ANCHO // 2 - 40, y + 11))

        hint = self.fuente_small.render("ESC o clic para cerrar", True, COLOR_SUBTITULO)
        self.ventana.blit(hint, hint.get_rect(center=(ANCHO // 2, ALTO // 2 + 155)))

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
                    if self.btn_niveles.fue_clickeado(evento):
                        return "niveles"
                    if self.btn_sapo.fue_clickeado(evento):
                        return "elegir_sapo"
                    if self.btn_controles.fue_clickeado(evento):
                        self.mostrar_controles = True
                    if self.btn_pantalla.fue_clickeado(evento):
                        return "toggle_pantalla"
                    if self.btn_salir.fue_clickeado(evento):
                        pygame.quit()
                        sys.exit()
                else:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        self.mostrar_controles = False

            # Dibujo
            if self.fondo:
                self.ventana.blit(self.fondo, (0, 0))
                self.ventana.blit(self.overlay, (0, 0))
            else:
                self.ventana.fill(COLOR_FONDO)

            titulo = self.fuente_titulo.render("El Sapo del Cafe", True, COLOR_TITULO)
            self.ventana.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 160)))

            sub = self.fuente_subtitulo.render("Sube hasta la cima!", True, COLOR_SUBTITULO)
            self.ventana.blit(sub, sub.get_rect(center=(ANCHO // 2, 228)))

            if not self.mostrar_controles:
                for boton in self.botones:
                    boton.actualizar(mouse_pos)
                    boton.dibujar(self.ventana, self.fuente_botones)
            else:
                self._dibujar_controles()

            pygame.display.flip()
            clock.tick(60)