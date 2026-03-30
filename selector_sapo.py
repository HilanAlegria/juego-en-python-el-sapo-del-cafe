# selector_sapo.py
import pygame
import sys
from config import ANCHO, ALTO, FUENTE_PATH

COLOR_FONDO     = (15, 25, 10)
COLOR_TITULO    = (255, 220, 50)
COLOR_TEXTO     = (220, 255, 220)
COLOR_SELECCION = (80, 200, 80)
COLOR_BORDE     = (50, 130, 50)
COLOR_HOVER     = (30, 80, 30)

SAPOS = [
    ("Verde",        "imagenes/frog_green_spritesheet.png"),
    ("Cafe",         "imagenes/frog_brown_spritesheet.png"),
    ("Azul",         "imagenes/frog_blue_spritesheet.png"),
    ("Morado",       "imagenes/frog_purple_spritesheet.png"),
    ("Cowboy",       "imagenes/frog_cowboy_spritesheet.png"),
    ("Viking",       "imagenes/frog_viking_spritesheet.png"),
    ("Pirata",       "imagenes/frog_pirate_spritesheet.png"),
    ("Tan Pirata",   "imagenes/frog_tan_pirate_spritesheet.png"),
    ("Tophat",       "imagenes/frog_tophat_spritesheet.png"),
    ("Payaso",       "imagenes/frog_clown_spritesheet.png"),
    ("Gafas",        "imagenes/frog_funnyglasses_spritesheet.png"),
    ("GameBoy",      "imagenes/frog_GameBoy_Green_spritesheet.png"),
]

SPRITE_W = 32
SPRITE_H = 32
COLS     = 8


class SelectorSapo:
    def __init__(self, ventana):
        self.ventana   = ventana
        self.seleccion = 0   # índice del sapo seleccionado
        self.hover     = -1

        self.fuente_titulo = pygame.font.Font(FUENTE_PATH, 20)
        self.fuente_nombre = pygame.font.Font(FUENTE_PATH, 10)
        self.fuente_hint   = pygame.font.Font(FUENTE_PATH, 9)

        # Precargar preview de cada sapo (frame 0, fila 0)
        self.previews = []
        for nombre, ruta in SAPOS:
            try:
                sheet = pygame.image.load(ruta).convert_alpha()
                frame = sheet.subsurface(pygame.Rect(0, 0, SPRITE_W, SPRITE_H))
                frame = pygame.transform.scale(frame, (64, 64))
                self.previews.append(frame)
            except:
                # Si no carga, superficie vacía
                surf = pygame.Surface((64, 64), pygame.SRCALPHA)
                self.previews.append(surf)

        # Fondo
        try:
            self.fondo = pygame.image.load("imagenes/fondo Level 1.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
            self.overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            self.overlay.fill((0, 0, 0, 170))
        except:
            self.fondo   = None
            self.overlay = None

        # Preview animado del sapo seleccionado
        self.frame_actual  = 0
        self.timer_anim    = 0
        self.VELOCIDAD_ANIM = 120  # ms por frame

        # Cargar sheet completo para la animación de preview
        self.sheet_actual = None
        self._cargar_sheet_actual()

    def _cargar_sheet_actual(self):
        try:
            ruta = SAPOS[self.seleccion][1]
            self.sheet_actual = pygame.image.load(ruta).convert_alpha()
        except:
            self.sheet_actual = None

    def _get_frame_animado(self):
        if not self.sheet_actual:
            return None
        rect = pygame.Rect(self.frame_actual * SPRITE_W, 0, SPRITE_W, SPRITE_H)
        frame = self.sheet_actual.subsurface(rect)
        return pygame.transform.scale(frame, (128, 128))

    def ejecutar(self):
        """
        Retorna la ruta del spritesheet elegido.
        """
        clock = pygame.time.Clock()

        # Layout: 4 columnas de sapos
        COLS_GRID = 4
        CARD_W, CARD_H = 130, 110
        GAP         = 16
        total_ancho = COLS_GRID * CARD_W + (COLS_GRID - 1) * GAP
        start_x     = ANCHO // 2 - total_ancho // 2
        start_y     = 180

        while True:
            dt        = clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            # Animación del preview
            self.timer_anim += dt
            if self.timer_anim >= self.VELOCIDAD_ANIM:
                self.frame_actual = (self.frame_actual + 1) % COLS
                self.timer_anim   = 0

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return SAPOS[0][1]  # default verde
                    if evento.key == pygame.K_RETURN:
                        return SAPOS[self.seleccion][1]
                    if evento.key == pygame.K_LEFT and self.seleccion > 0:
                        self.seleccion -= 1
                        self.frame_actual = 0
                        self._cargar_sheet_actual()
                    if evento.key == pygame.K_RIGHT and self.seleccion < len(SAPOS) - 1:
                        self.seleccion += 1
                        self.frame_actual = 0
                        self._cargar_sheet_actual()

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    # Ver si clickeó una card
                    for i, _ in enumerate(SAPOS):
                        fila = i // COLS_GRID
                        col  = i % COLS_GRID
                        x    = start_x + col * (CARD_W + GAP)
                        y    = start_y + fila * (CARD_H + GAP)
                        rect = pygame.Rect(x, y, CARD_W, CARD_H)
                        if rect.collidepoint(evento.pos):
                            if self.seleccion == i:
                                # Doble click / ya estaba seleccionado → confirmar
                                return SAPOS[self.seleccion][1]
                            else:
                                self.seleccion = i
                                self.frame_actual = 0
                                self._cargar_sheet_actual()

                    # Botón confirmar
                    btn_confirmar = pygame.Rect(ANCHO // 2 - 150, ALTO - 80, 300, 50)
                    if btn_confirmar.collidepoint(evento.pos):
                        return SAPOS[self.seleccion][1]

            # --- Dibujo ---
            if self.fondo:
                self.ventana.blit(self.fondo, (0, 0))
                self.ventana.blit(self.overlay, (0, 0))
            else:
                self.ventana.fill(COLOR_FONDO)

            # Título
            titulo = self.fuente_titulo.render("ELIGE TU SAPO", True, COLOR_TITULO)
            self.ventana.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 80)))

            # Preview animado del seleccionado
            frame_anim = self._get_frame_animado()
            if frame_anim:
                self.ventana.blit(frame_anim, frame_anim.get_rect(center=(ANCHO // 2, 138)))

            # Grid de sapos
            self.hover = -1
            for i, (nombre, ruta) in enumerate(SAPOS):
                fila = i // COLS_GRID
                col  = i % COLS_GRID
                x    = start_x + col * (CARD_W + GAP)
                y    = start_y + fila * (CARD_H + GAP)
                rect = pygame.Rect(x, y, CARD_W, CARD_H)

                es_seleccionado = (i == self.seleccion)
                es_hover        = rect.collidepoint(mouse_pos)
                if es_hover:
                    self.hover = i

                # Fondo de la card
                if es_seleccionado:
                    pygame.draw.rect(self.ventana, COLOR_SELECCION, rect, border_radius=10)
                elif es_hover:
                    pygame.draw.rect(self.ventana, COLOR_HOVER, rect, border_radius=10)
                else:
                    pygame.draw.rect(self.ventana, (20, 50, 20), rect, border_radius=10)

                # Borde
                borde_color = (255, 220, 0) if es_seleccionado else COLOR_BORDE
                pygame.draw.rect(self.ventana, borde_color, rect, 2, border_radius=10)

                # Preview del sapo
                preview = self.previews[i]
                preview_rect = preview.get_rect(center=(x + CARD_W // 2, y + CARD_H // 2 - 10))
                self.ventana.blit(preview, preview_rect)

                # Nombre
                nombre_surf = self.fuente_nombre.render(nombre.upper(), True, COLOR_TEXTO)
                self.ventana.blit(nombre_surf, nombre_surf.get_rect(center=(x + CARD_W // 2, y + CARD_H - 18)))

            # Botón confirmar
            btn = pygame.Rect(ANCHO // 2 - 150, ALTO - 80, 300, 50)
            btn_hover = btn.collidepoint(mouse_pos)
            pygame.draw.rect(self.ventana, (50, 130, 50) if btn_hover else (30, 80, 30), btn, border_radius=12)
            pygame.draw.rect(self.ventana, COLOR_SELECCION, btn, 2, border_radius=12)
            confirmar = self.fuente_nombre.render("JUGAR CON ESTE SAPO", True, COLOR_TEXTO)
            self.ventana.blit(confirmar, confirmar.get_rect(center=btn.center))

            # Hint
            hint = self.fuente_hint.render("CLIC para seleccionar  |  ENTER para confirmar", True, (120, 180, 120))
            self.ventana.blit(hint, hint.get_rect(center=(ANCHO // 2, ALTO - 20)))

            pygame.display.flip()