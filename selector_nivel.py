# selector_nivel.py
import pygame
import sys
from config import ANCHO, ALTO, FUENTE_PATH
from progreso import cargar_progreso

COLOR_FONDO          = (15, 25, 10)
COLOR_TITULO         = (255, 220, 50)
COLOR_TEXTO          = (220, 255, 220)
COLOR_BTN            = (30, 80, 30)
COLOR_BTN_HOVER      = (50, 130, 50)
COLOR_BTN_BORDE      = (80, 180, 80)
COLOR_BLOQUEADO      = (40, 40, 40)
COLOR_BORDE_BLOQ     = (70, 70, 70)
COLOR_TEXTO_BLOQ     = (90, 90, 90)

NIVELES_INFO = [
    {
        "numero"  : 1,
        "titulo"  : "NIVEL 1",
        "subtitulo": "LA CUEVA",
        "desc"    : "Salta entre rocas\npara salir de la cueva",
    },
    {
        "numero"  : 2,
        "titulo"  : "NIVEL 2",
        "subtitulo": "LA SUPERFICIE",
        "desc"    : "Sube por la tierra\nhacia el bosque",
    },
    {
        "numero"  : 3,
        "titulo"  : "NIVEL 3",
        "subtitulo": "LOS ARBOLES",
        "desc"    : "Salta entre ramas\nhasta la cima",
    },
]


class SelectorNivel:
    def __init__(self, ventana):
        self.ventana = ventana

        self.fuente_titulo   = pygame.font.Font(FUENTE_PATH, 20)
        self.fuente_nivel    = pygame.font.Font(FUENTE_PATH, 13)
        self.fuente_sub      = pygame.font.Font(FUENTE_PATH, 9)
        self.fuente_desc     = pygame.font.Font(FUENTE_PATH, 8)
        self.fuente_hint     = pygame.font.Font(FUENTE_PATH, 8)

        try:
            self.fondo = pygame.image.load("imagenes/fondo Level 1.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
            self.overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            self.overlay.fill((0, 0, 0, 180))
        except:
            self.fondo   = None
            self.overlay = None

    def ejecutar(self):
        """
        Retorna el índice del nivel elegido (0, 1, 2)
        o None si el jugador cancela con ESC.
        """
        clock = pygame.time.Clock()

        CARD_W, CARD_H = 300, 260
        GAP     = 40
        total_w = len(NIVELES_INFO) * CARD_W + (len(NIVELES_INFO) - 1) * GAP
        start_x = ANCHO // 2 - total_w // 2
        start_y = ALTO  // 2 - CARD_H // 2 + 30

        while True:
            desbloqueados = cargar_progreso()
            mouse_pos     = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for i, info in enumerate(NIVELES_INFO):
                        x    = start_x + i * (CARD_W + GAP)
                        rect = pygame.Rect(x, start_y, CARD_W, CARD_H)
                        if rect.collidepoint(evento.pos) and i < desbloqueados:
                            return i

            # --- Dibujo ---
            if self.fondo:
                self.ventana.blit(self.fondo, (0, 0))
                self.ventana.blit(self.overlay, (0, 0))
            else:
                self.ventana.fill(COLOR_FONDO)

            # Título
            titulo = self.fuente_titulo.render("SELECCIONA NIVEL", True, COLOR_TITULO)
            self.ventana.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 120)))

            # Cards de niveles
            for i, info in enumerate(NIVELES_INFO):
                x            = start_x + i * (CARD_W + GAP)
                rect         = pygame.Rect(x, start_y, CARD_W, CARD_H)
                desbloqueado = i < desbloqueados
                es_hover     = rect.collidepoint(mouse_pos) and desbloqueado

                # Fondo de la card
                if not desbloqueado:
                    pygame.draw.rect(self.ventana, COLOR_BLOQUEADO, rect, border_radius=14)
                    pygame.draw.rect(self.ventana, COLOR_BORDE_BLOQ, rect, 2, border_radius=14)
                elif es_hover:
                    pygame.draw.rect(self.ventana, COLOR_BTN_HOVER, rect, border_radius=14)
                    pygame.draw.rect(self.ventana, COLOR_BTN_BORDE, rect, 2, border_radius=14)
                else:
                    pygame.draw.rect(self.ventana, COLOR_BTN, rect, border_radius=14)
                    pygame.draw.rect(self.ventana, COLOR_BTN_BORDE, rect, 2, border_radius=14)

                color_texto = COLOR_TEXTO_BLOQ if not desbloqueado else COLOR_TEXTO
                color_sub   = (60, 60, 60) if not desbloqueado else (150, 220, 100)

                # Número de nivel
                num = self.fuente_nivel.render(info["titulo"], True, color_texto)
                self.ventana.blit(num, num.get_rect(center=(x + CARD_W // 2, start_y + 60)))

                # Subtítulo
                sub = self.fuente_sub.render(info["subtitulo"], True, color_sub)
                self.ventana.blit(sub, sub.get_rect(center=(x + CARD_W // 2, start_y + 100)))

                # Separador
                if desbloqueado:
                    pygame.draw.line(
                        self.ventana, COLOR_BTN_BORDE,
                        (x + 20, start_y + 125),
                        (x + CARD_W - 20, start_y + 125), 1
                    )

                # Descripción (2 líneas)
                if desbloqueado:
                    for j, linea in enumerate(info["desc"].split("\n")):
                        d = self.fuente_desc.render(linea, True, color_texto)
                        self.ventana.blit(d, d.get_rect(
                            center=(x + CARD_W // 2, start_y + 155 + j * 22)
                        ))
                else:
                    # Candado visual dibujado con formas
                    self._dibujar_candado(x + CARD_W // 2, start_y + CARD_H // 2 + 10)

            # Hint
            hint = self.fuente_hint.render("ESC para volver", True, (100, 150, 100))
            self.ventana.blit(hint, hint.get_rect(center=(ANCHO // 2, ALTO - 40)))

            pygame.display.flip()
            clock.tick(60)

    def _dibujar_candado(self, cx, cy):
        """Dibuja un candado simple con formas geométricas."""
        color = (80, 80, 80)
        # Cuerpo del candado
        pygame.draw.rect(self.ventana, color,
                         pygame.Rect(cx - 18, cy - 5, 36, 28), border_radius=4)
        # Arco superior
        pygame.draw.arc(self.ventana, color,
                        pygame.Rect(cx - 14, cy - 28, 28, 30),
                        0, 3.14159, 4)
        # Ojo del candado
        pygame.draw.circle(self.ventana, (50, 50, 50), (cx, cy + 8), 6)