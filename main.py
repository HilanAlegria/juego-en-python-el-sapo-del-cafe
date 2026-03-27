import pygame
import sys
from config import *
from player import Player
from camera import Camera
from level import cargar_nivel1

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Platformer 2D - Nivel con Cámara")
clock = pygame.time.Clock()

# --- Cargar recursos ---
fondo = pygame.image.load("imagenes/fondo Level 1.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# --- Cargar nivel ---
platforms, ancho_nivel, alto_nivel = cargar_nivel1()

# --- Punto de spawn (reutilizable para respawn) ---
SPAWN_X, SPAWN_Y = 100, alto_nivel - 150

# --- Crear entidades ---
jugador = Player(SPAWN_X, SPAWN_Y)
camera = Camera(ancho_nivel, alto_nivel)

# --- Bucle principal ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    # --- Lógica del jugador ---
    dx = jugador.handle_input(teclas)
    jugador.jump(teclas)
    jugador.apply_gravity()
    jugador.move(dx, platforms, alto_nivel)

    # Clamp horizontal: evitar salir del nivel
    jugador.rect.left = max(0, jugador.rect.left)
    jugador.rect.right = min(ancho_nivel, jugador.rect.right)

    # Respawn si cae fuera del nivel verticalmente
    if jugador.rect.top > alto_nivel:
        jugador.rect.topleft = (SPAWN_X, SPAWN_Y)
        jugador.vel_y = 0

    # --- Actualizar cámara ---
    camera.update(jugador)

    # --- Dibujar ---
    ventana.blit(fondo, (0, 0))

    for plat in platforms:
        rect_cam = camera.aplicar(plat)
        pygame.draw.rect(ventana, GRIS, rect_cam)

    jugador_rect_cam = camera.aplicar(jugador)
    ventana.blit(jugador.image, jugador_rect_cam)

    pygame.display.flip()
    clock.tick(FPS)