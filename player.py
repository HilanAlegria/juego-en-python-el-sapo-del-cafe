# player.py
import pygame
from config import VELOCIDAD_JUGADOR, GRAVEDAD, FUERZA_SALTO

VIDAS_MAX    = 3
UMBRAL_CAIDA = 260
SPRITE_W     = 32
SPRITE_H     = 32
COLS         = 8

FILA_CAMINAR = 0
FILA_SALTAR  = 1
FILA_CAER    = 2


class Player:
    def __init__(self, x, y, spritesheet_path="imagenes/frog_green_spritesheet.png"):
        self.spritesheet_path = spritesheet_path
        self._cargar_spritesheet(spritesheet_path)

        self.rect = pygame.Rect(x, y, 64, 64)

        # Físicas
        self.vel_y           = 0
        self.en_suelo        = False
        self.mirando_derecha = True

        # Vidas
        self.vidas = VIDAS_MAX

        # Invencibilidad
        self.invencible        = False
        self.frames_invencible = 0
        self.DURACION_INV      = 90

        # Caída
        self._cayendo        = False
        self._y_inicio_caida = 0
        self._caida_fatal    = False

        # Animación
        self.frame_actual   = 0
        self.timer_anim     = 0
        self.VELOCIDAD_ANIM = 100
        self.fila_actual    = FILA_CAMINAR

        # Inicializar image desde el inicio para evitar AttributeError
        self.image = self.frames[FILA_CAMINAR][0]

    def _cargar_spritesheet(self, path):
        sheet = pygame.image.load(path).convert_alpha()
        self.frames = {}
        for fila in range(4):
            self.frames[fila] = []
            for col in range(COLS):
                rect  = pygame.Rect(col * SPRITE_W, fila * SPRITE_H, SPRITE_W, SPRITE_H)
                frame = sheet.subsurface(rect)
                frame = pygame.transform.scale(frame, (64, 64))
                self.frames[fila].append(frame)

    def cambiar_skin(self, path):
        self._cargar_spritesheet(path)
        self.image = self.frames[FILA_CAMINAR][0]

    # ------------------------------------------------------------------ #
    #  Vidas                                                               #
    # ------------------------------------------------------------------ #
    def perder_vida(self, spawn_x, spawn_y):
        if self.invencible:
            return
        self.vidas            -= 1
        self.rect.topleft      = (spawn_x, spawn_y)
        self.vel_y             = 0
        self.en_suelo          = False
        self._cayendo          = False
        self._y_inicio_caida   = 0
        self.invencible        = True
        self.frames_invencible = self.DURACION_INV

    def esta_muerto(self):
        return self.vidas <= 0

    # ------------------------------------------------------------------ #
    #  Input                                                               #
    # ------------------------------------------------------------------ #
    def handle_input(self, teclas):
        dx = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -VELOCIDAD_JUGADOR
            self.mirando_derecha = False
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = VELOCIDAD_JUGADOR
            self.mirando_derecha = True
        return dx

    def jump(self, teclas):
        saltar = (
            teclas[pygame.K_SPACE] or
            teclas[pygame.K_UP]    or
            teclas[pygame.K_w]
        )
        if saltar and self.en_suelo:
            self.vel_y    = -FUERZA_SALTO
            self.en_suelo = False

    # ------------------------------------------------------------------ #
    #  Física                                                              #
    # ------------------------------------------------------------------ #
    def apply_gravity(self):
        self.vel_y += GRAVEDAD
        if self.vel_y > 20:
            self.vel_y = 20

    def move(self, dx, platforms, alto_nivel):
        # --- Horizontal ---
        self.rect.x += dx
        for plat in platforms:
            if self.rect.colliderect(plat):
                if dx > 0:
                    self.rect.right = plat.left
                elif dx < 0:
                    self.rect.left  = plat.right

        # --- Vertical ---
        self.rect.y += self.vel_y
        estaba_en_suelo        = self.en_suelo
        self.en_suelo          = False
        aterizzo_en_plataforma = False

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:
                    self.rect.bottom       = plat.top
                    self.vel_y             = 0
                    self.en_suelo          = True
                    aterizzo_en_plataforma = True
                elif self.vel_y < 0:
                    self.rect.top = plat.bottom
                    self.vel_y    = 0

        toco_suelo = False
        if self.rect.bottom >= alto_nivel:
            self.rect.bottom = alto_nivel
            self.vel_y       = 0
            self.en_suelo    = True
            toco_suelo       = True

        # --- Lógica caída fatal ---
        if estaba_en_suelo and not self.en_suelo:
            self._cayendo        = True
            self._y_inicio_caida = self.rect.y

        if self.en_suelo and self._cayendo:
            distancia_caida = self.rect.y - self._y_inicio_caida
            self._cayendo   = False
            if (toco_suelo or aterizzo_en_plataforma) and distancia_caida > UMBRAL_CAIDA:
                self._caida_fatal = True
            else:
                self._caida_fatal = False
        else:
            self._caida_fatal = False

    # ------------------------------------------------------------------ #
    #  Update — animación e invencibilidad                                 #
    # ------------------------------------------------------------------ #
    def update(self, dt, dx):
        # --- Elegir fila de animación ---
        nueva_fila = self.fila_actual

        if not self.en_suelo:
            if self.vel_y < 0:
                nueva_fila = FILA_SALTAR
            else:
                nueva_fila = FILA_CAER
        else:
            nueva_fila = FILA_CAMINAR

        # Si cambió la fila resetear frame para evitar IndexError
        if nueva_fila != self.fila_actual:
            self.fila_actual  = nueva_fila
            self.frame_actual = 0
            self.timer_anim   = 0
        else:
            self.fila_actual = nueva_fila

        # --- Avanzar frame ---
        self.timer_anim += dt
        if self.timer_anim >= self.VELOCIDAD_ANIM:
            num_frames        = len(self.frames[self.fila_actual])
            self.frame_actual = (self.frame_actual + 1) % num_frames
            self.timer_anim   = 0

        # --- Obtener imagen y voltear si va a la izquierda ---
        frame = self.frames[self.fila_actual][self.frame_actual]
        if not self.mirando_derecha:
            frame = pygame.transform.flip(frame, True, False)

        # --- Invencibilidad / parpadeo ---
        if self.invencible:
            self.frames_invencible -= 1
            if (self.frames_invencible // 6) % 2 == 0:
                frame = frame.copy()
                frame.set_alpha(80)
            if self.frames_invencible <= 0:
                self.invencible = False

        self.image = frame