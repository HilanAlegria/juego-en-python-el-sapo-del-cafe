# player.py
import pygame
from config import GRAVEDAD, FUERZA_SALTO, VEL_MAX_JUGADOR, ACELERACION, FRICCION

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
        self.vel_x           = 0.0   # ahora es float para inercia suave
        self.vel_y           = 0.0
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
        self._y_inicio_caida = 0.0
        self._caida_fatal    = False

        # Animación
        self.frame_actual   = 0
        self.timer_anim     = 0
        self.VELOCIDAD_ANIM = 100
        self.fila_actual    = FILA_CAMINAR

        # Squash y stretch
        self.squash_timer    = 0       # frames que dura el efecto
        self.squash_scale_x  = 1.0    # escala horizontal
        self.squash_scale_y  = 1.0    # escala vertical

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
    #  Squash y stretch                                                    #
    # ------------------------------------------------------------------ #
    def _activar_squash(self, tipo):
        """
        tipo 'salto'    → se estira verticalmente al saltar
        tipo 'aterrizaje' → se aplana al caer
        """
        if tipo == "salto":
            self.squash_scale_x = 0.7
            self.squash_scale_y = 1.4
        elif tipo == "aterrizaje":
            self.squash_scale_x = 1.4
            self.squash_scale_y = 0.7
        self.squash_timer = 8   # dura 8 frames

    def _actualizar_squash(self):
        if self.squash_timer > 0:
            self.squash_timer -= 1
            # Interpola de vuelta a 1.0 gradualmente
            t = self.squash_timer / 8
            self.squash_scale_x = 1.0 + (self.squash_scale_x - 1.0) * t
            self.squash_scale_y = 1.0 + (self.squash_scale_y - 1.0) * t
        else:
            self.squash_scale_x = 1.0
            self.squash_scale_y = 1.0

    # ------------------------------------------------------------------ #
    #  Vidas                                                               #
    # ------------------------------------------------------------------ #
    def perder_vida(self, spawn_x, spawn_y):
        if self.invencible:
            return
        self.vidas            -= 1
        self.rect.topleft      = (spawn_x, spawn_y)
        self.vel_x             = 0.0
        self.vel_y             = 0.0
        self.en_suelo          = False
        self._cayendo          = False
        self._y_inicio_caida   = 0.0
        self.invencible        = True
        self.frames_invencible = self.DURACION_INV

    def esta_muerto(self):
        return self.vidas <= 0

    # ------------------------------------------------------------------ #
    #  Input con inercia                                                   #
    # ------------------------------------------------------------------ #
    def handle_input(self, teclas):
        """
        Ya no retorna dx directamente.
        Aplica aceleración y fricción a self.vel_x.
        Retorna vel_x para que main.py sepa la dirección.
        """
        moviendo = False

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vel_x      -= ACELERACION
            self.mirando_derecha = False
            moviendo         = True
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel_x      += ACELERACION
            self.mirando_derecha = True
            moviendo         = True

        # Aplicar fricción cuando no hay input
        if not moviendo:
            self.vel_x *= FRICCION

        # Clamp a velocidad máxima
        self.vel_x = max(-VEL_MAX_JUGADOR, min(VEL_MAX_JUGADOR, self.vel_x))

        # Si la velocidad es muy pequeña, parar completamente
        if abs(self.vel_x) < 0.2:
            self.vel_x = 0.0

        return self.vel_x

    def jump(self, teclas):
        saltar = (
            teclas[pygame.K_SPACE] or
            teclas[pygame.K_UP]    or
            teclas[pygame.K_w]
        )
        if saltar and self.en_suelo:
            self.vel_y    = -FUERZA_SALTO
            self.en_suelo = False
            self._activar_squash("salto")

    def apply_gravity(self):
        self.vel_y += GRAVEDAD
        if self.vel_y > 20:
            self.vel_y = 20

    def move(self, platforms, alto_nivel):
        """
        Ahora usa self.vel_x internamente en lugar de recibir dx.
        """
        dx = int(self.vel_x)

        # --- Horizontal ---
        self.rect.x += dx
        for plat in platforms:
            if self.rect.colliderect(plat):
                if dx > 0:
                    self.rect.right = plat.left
                    self.vel_x      = 0.0
                elif dx < 0:
                    self.rect.left  = plat.right
                    self.vel_x      = 0.0

        # --- Vertical ---
        self.rect.y      += int(self.vel_y)
        estaba_en_suelo   = self.en_suelo
        self.en_suelo     = False
        aterrizó          = False

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:
                    self.rect.bottom = plat.top
                    self.vel_y       = 0.0
                    self.en_suelo    = True
                    aterrizó         = True
                elif self.vel_y < 0:
                    self.rect.top = plat.bottom
                    self.vel_y    = 0.0

        toco_suelo = False
        if self.rect.bottom >= alto_nivel:
            self.rect.bottom = alto_nivel
            self.vel_y       = 0.0
            self.en_suelo    = True
            toco_suelo       = True
            aterrizó         = True

        # Squash al aterrizar
        if aterrizó and not estaba_en_suelo:
            self._activar_squash("aterrizaje")

        # --- Lógica caída fatal ---
        if estaba_en_suelo and not self.en_suelo:
            self._cayendo        = True
            self._y_inicio_caida = float(self.rect.y)

        if self.en_suelo and self._cayendo:
            distancia = self.rect.y - self._y_inicio_caida
            self._cayendo = False
            self._caida_fatal = (distancia > UMBRAL_CAIDA)
        else:
            if not self._cayendo:
                self._caida_fatal = False

    # ------------------------------------------------------------------ #
    #  Update                                                              #
    # ------------------------------------------------------------------ #
    def update(self, dt):
        # --- Elegir fila ---
        nueva_fila = self.fila_actual
        if not self.en_suelo:
            nueva_fila = FILA_SALTAR if self.vel_y < 0 else FILA_CAER
        else:
            nueva_fila = FILA_CAMINAR

        if nueva_fila != self.fila_actual:
            self.fila_actual  = nueva_fila
            self.frame_actual = 0
            self.timer_anim   = 0
        
        # --- Avanzar frame ---
        self.timer_anim += dt
        if self.timer_anim >= self.VELOCIDAD_ANIM:
            num_frames        = len(self.frames[self.fila_actual])
            self.frame_actual = (self.frame_actual + 1) % num_frames
            self.timer_anim   = 0

        # --- Squash/stretch ---
        self._actualizar_squash()

        # --- Construir imagen final ---
        frame = self.frames[self.fila_actual][self.frame_actual]

        # Aplicar squash/stretch si hay efecto activo
        if self.squash_scale_x != 1.0 or self.squash_scale_y != 1.0:
            nuevo_w = int(64 * self.squash_scale_x)
            nuevo_h = int(64 * self.squash_scale_y)
            nuevo_w = max(1, nuevo_w)
            nuevo_h = max(1, nuevo_h)
            frame   = pygame.transform.scale(frame, (nuevo_w, nuevo_h))

        if not self.mirando_derecha:
            frame = pygame.transform.flip(frame, True, False)

        # --- Invencibilidad ---
        if self.invencible:
            self.frames_invencible -= 1
            if (self.frames_invencible // 6) % 2 == 0:
                frame = frame.copy()
                frame.set_alpha(80)
            if self.frames_invencible <= 0:
                self.invencible = False

        self.image = frame