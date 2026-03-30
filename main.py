# main.py
import pygame
import sys
from config import *
from player import Player
from camera import Camera
from level import cargar_nivel1
from menu import Menu
from hud import HUD
from gameover import PantallaGameOver
from victoria import PantallaVictoria
from selector_sapo import SelectorSapo

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El Sapo del Cafe")
clock = pygame.time.Clock()

# Sapo elegido por defecto
sapo_path = "imagenes/frog_green_spritesheet.png"

# ------------------------------------------------------------------ #
#  Función para reiniciar el estado del juego                          #
# ------------------------------------------------------------------ #
def iniciar_juego(spritesheet_path):
    platforms, zona_meta, ancho_nivel, alto_nivel = cargar_nivel1()
    spawn_x, spawn_y = 100, alto_nivel - 150
    jugador  = Player(spawn_x, spawn_y, spritesheet_path)
    camera   = Camera(ancho_nivel, alto_nivel)
    return platforms, zona_meta, ancho_nivel, alto_nivel, spawn_x, spawn_y, jugador, camera

# ------------------------------------------------------------------ #
#  Menú principal                                                      #
# ------------------------------------------------------------------ #
def mostrar_menu():
    global sapo_path
    while True:
        menu      = Menu(ventana)
        resultado = menu.ejecutar()
        if resultado == "jugar":
            return
        elif resultado == "elegir_sapo":
            selector  = SelectorSapo(ventana)
            sapo_path = selector.ejecutar()
        else:
            pygame.quit()
            sys.exit()

mostrar_menu()

# ------------------------------------------------------------------ #
#  Cargar recursos                                                     #
# ------------------------------------------------------------------ #
fondo = pygame.image.load("imagenes/fondo Level 1.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

hud = HUD(vidas_max=3)

platforms, zona_meta, ancho_nivel, alto_nivel, SPAWN_X, SPAWN_Y, jugador, camera = iniciar_juego(sapo_path)

# ------------------------------------------------------------------ #
#  Bucle principal                                                     #
# ------------------------------------------------------------------ #
while True:
    dt = clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                mostrar_menu()
                platforms, zona_meta, ancho_nivel, alto_nivel, SPAWN_X, SPAWN_Y, jugador, camera = iniciar_juego(sapo_path)

    teclas = pygame.key.get_pressed()

    # --- Lógica ---
    dx = jugador.handle_input(teclas)
    jugador.jump(teclas)
    jugador.apply_gravity()
    jugador.move(dx, platforms, alto_nivel)
    jugador.update(dt, dx)

    # Clamp horizontal
    jugador.rect.left  = max(0, jugador.rect.left)
    jugador.rect.right = min(ancho_nivel, jugador.rect.right)

    # Caída fuera del nivel
    if jugador.rect.top > alto_nivel:
        jugador.perder_vida(SPAWN_X, SPAWN_Y)

    # Caída fatal por físicas
    if jugador._caida_fatal:
        jugador.perder_vida(SPAWN_X, SPAWN_Y)
        jugador._caida_fatal = False

    # --- Detectar victoria ---
    if jugador.rect.colliderect(zona_meta):
        captura    = ventana.copy()
        pantalla_v = PantallaVictoria(ventana, captura, jugador.vidas)
        resultado  = pantalla_v.ejecutar()

        if resultado == "siguiente":
            mostrar_menu()
            platforms, zona_meta, ancho_nivel, alto_nivel, SPAWN_X, SPAWN_Y, jugador, camera = iniciar_juego(sapo_path)
        elif resultado == "menu":
            mostrar_menu()
            platforms, zona_meta, ancho_nivel, alto_nivel, SPAWN_X, SPAWN_Y, jugador, camera = iniciar_juego(sapo_path)

    # --- Verificar game over ---
    if jugador.esta_muerto():
        captura     = ventana.copy()
        pantalla_go = PantallaGameOver(ventana, captura)
        resultado   = pantalla_go.ejecutar()

        if resultado == "reintentar":
            platforms, zona_meta, ancho_nivel, alto_nivel, SPAWN_X, SPAWN_Y, jugador, camera = iniciar_juego(sapo_path)
        elif resultado == "menu":
            mostrar_menu()
            platforms, zona_meta, ancho_nivel, alto_nivel, SPAWN_X, SPAWN_Y, jugador, camera = iniciar_juego(sapo_path)

    # --- Cámara ---
    camera.update(jugador)

    # --- Dibujo ---
    ventana.blit(fondo, (0, 0))

    for plat in platforms:
        rect_cam = camera.aplicar(plat)
        pygame.draw.rect(ventana, GRIS, rect_cam)

    # Zona de meta
    meta_cam  = camera.aplicar(zona_meta)
    meta_surf = pygame.Surface((meta_cam.width, meta_cam.height), pygame.SRCALPHA)
    meta_surf.fill((50, 220, 80, 100))
    ventana.blit(meta_surf, meta_cam)
    pygame.draw.rect(ventana, (50, 220, 80), meta_cam, 2, border_radius=6)

    jugador_rect_cam = camera.aplicar(jugador)
    ventana.blit(jugador.image, jugador_rect_cam)

    # HUD siempre encima de todo
    hud.dibujar(ventana, jugador.vidas)

    pygame.display.flip()