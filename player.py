import pygame
from config import VELOCIDAD_JUGADOR, GRAVEDAD, FUERZA_SALTO

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("imagenes/sapa.PNG").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Físicas
        self.vel_y = 0
        self.en_suelo = False

    def handle_input(self, teclas):
        dx = 0
        if teclas[pygame.K_LEFT]:
            dx = -VELOCIDAD_JUGADOR
        if teclas[pygame.K_RIGHT]:
            dx = VELOCIDAD_JUGADOR
        return dx

    def jump(self, teclas):
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = -FUERZA_SALTO
            self.en_suelo = False

    def apply_gravity(self):
        self.vel_y += GRAVEDAD
        if self.vel_y > 20:
            self.vel_y = 20

    def move(self, dx, platforms, alto_nivel):
        # --- Movimiento horizontal ---
        self.rect.x += dx
        for plat in platforms:
            if self.rect.colliderect(plat):
                if dx > 0:
                    self.rect.right = plat.left
                elif dx < 0:
                    self.rect.left = plat.right

        # --- Movimiento vertical ---
        self.rect.y += self.vel_y
        self.en_suelo = False

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:
                    # Cayendo: apoyar encima de la plataforma
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.en_suelo = True
                elif self.vel_y < 0:
                    # Saltando: rebotar contra el techo
                    self.rect.top = plat.bottom
                    self.vel_y = 0

        # Límite inferior del nivel
        if self.rect.bottom >= alto_nivel:
            self.rect.bottom = alto_nivel
            self.vel_y = 0
            self.en_suelo = True