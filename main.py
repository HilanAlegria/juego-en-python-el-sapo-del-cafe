# main.py
import pygame
import sys
from config import *
from player import Player
from camera import Camera
from level import dibujar_plataformas
from menu import Menu
from hud import HUD
from gameover import PantallaGameOver
from victoria import PantallaVictoria
from selector_sapo import SelectorSapo
from selector_nivel import SelectorNivel
from parallax import Parallax
from progreso import cargar_progreso, desbloquear_siguiente
from nivel1 import cargar_nivel as cargar_nivel1
from nivel2 import cargar_nivel as cargar_nivel2
from nivel3 import cargar_nivel as cargar_nivel3

pygame.init()

# ------------------------------------------------------------------ #
#  Resolución                                                          #
# ------------------------------------------------------------------ #
info_monitor      = pygame.display.Info()
ANCHO_MONITOR     = info_monitor.current_w
ALTO_MONITOR      = info_monitor.current_h
pantalla_completa = False


def crear_ventana(completa):
    if completa:
        v = pygame.display.set_mode(
            (ANCHO_MONITOR, ALTO_MONITOR),
            pygame.FULLSCREEN
        )
    else:
        ancho = int(ANCHO_MONITOR * 0.85)
        alto  = int(ancho * 9 / 16)
        if alto > int(ALTO_MONITOR * 0.85):
            alto  = int(ALTO_MONITOR * 0.85)
            ancho = int(alto * 16 / 9)
        v = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("El Sapo del Cafe")
    return v


ventana      = crear_ventana(pantalla_completa)
clock        = pygame.time.Clock()
sapo_path    = "imagenes/frog_green_spritesheet.png"
nivel_actual = 0
NIVELES      = [cargar_nivel1, cargar_nivel2, cargar_nivel3]
parallax     = Parallax()
hud          = HUD(vidas_max=3)


# ------------------------------------------------------------------ #
#  Iniciar juego                                                       #
# ------------------------------------------------------------------ #
def iniciar_juego(spritesheet_path, num_nivel):
    datos            = NIVELES[num_nivel]()
    spawn_x, spawn_y = datos["spawn"]
    jugador          = Player(spawn_x, spawn_y, spritesheet_path)
    camera           = Camera(datos["ancho_nivel"], datos["alto_nivel"])
    parallax.cargar_capas(datos["capas_fondo"])
    return datos, jugador, camera


# ------------------------------------------------------------------ #
#  Menú                                                                #
# ------------------------------------------------------------------ #
def mostrar_menu():
    global sapo_path, nivel_actual, ventana, pantalla_completa
    while True:
        menu      = Menu(ventana, pantalla_completa)
        resultado = menu.ejecutar()

        if resultado == "jugar":
            return
        elif resultado == "niveles":
            selector = SelectorNivel(ventana)
            eleccion = selector.ejecutar()
            if eleccion is not None:
                nivel_actual = eleccion
                return
        elif resultado == "elegir_sapo":
            selector  = SelectorSapo(ventana)
            sapo_path = selector.ejecutar()
        elif resultado == "toggle_pantalla":
            pantalla_completa = not pantalla_completa
            ventana = crear_ventana(pantalla_completa)
        else:
            pygame.quit()
            sys.exit()


mostrar_menu()
datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)

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
                datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)

    teclas = pygame.key.get_pressed()

    platforms        = datos["plataformas"]
    suelo            = datos["suelo"]
    zona_meta        = datos["zona_meta"]
    ancho_nivel      = datos["ancho_nivel"]
    alto_nivel       = datos["alto_nivel"]
    spawn_x, spawn_y = datos["spawn"]

    # --- Lógica ---
    dx = jugador.handle_input(teclas)
    jugador.jump(teclas)
    jugador.apply_gravity()
    jugador.move(dx, [*platforms, suelo], alto_nivel)
    jugador.update(dt, dx)

    jugador.rect.left  = max(0, jugador.rect.left)
    jugador.rect.right = min(ancho_nivel, jugador.rect.right)

    if jugador.rect.top > alto_nivel:
        jugador.perder_vida(spawn_x, spawn_y)

    if jugador._caida_fatal:
        jugador.perder_vida(spawn_x, spawn_y)
        jugador._caida_fatal = False

    # --- Victoria ---
    if jugador.rect.colliderect(zona_meta):
        desbloquear_siguiente(nivel_actual, len(NIVELES))
        captura    = ventana.copy()
        pantalla_v = PantallaVictoria(ventana, captura, jugador.vidas)
        resultado  = pantalla_v.ejecutar()

        if resultado == "siguiente":
            if nivel_actual < len(NIVELES) - 1:
                vidas_ant    = jugador.vidas
                nivel_actual += 1
                datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)
                jugador.vidas = vidas_ant
            else:
                mostrar_menu()
                nivel_actual = 0
                datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)
        elif resultado == "menu":
            mostrar_menu()
            datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)

    # --- Game Over ---
    if jugador.esta_muerto():
        captura     = ventana.copy()
        pantalla_go = PantallaGameOver(ventana, captura)
        resultado   = pantalla_go.ejecutar()

        if resultado == "reintentar":
            datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)
        elif resultado == "menu":
            mostrar_menu()
            datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)

    # --- Cámara ---
    camera.update(jugador)

    # --- Dibujo ---
    # Fondo negro simple
    ventana.fill((10, 10, 10))

    # Plataformas y suelo
    dibujar_plataformas(
        ventana, platforms, suelo, camera,
        datos["tile_plat"], datos["tile_suelo"], GRIS
    )

    # Zona de meta
    meta_cam  = camera.aplicar(zona_meta)
    meta_surf = pygame.Surface((meta_cam.width, meta_cam.height), pygame.SRCALPHA)
    meta_surf.fill((50, 220, 80, 100))
    ventana.blit(meta_surf, meta_cam)
    pygame.draw.rect(ventana, (50, 220, 80), meta_cam, 2, border_radius=6)

    # Jugador
    jugador_rect_cam = camera.aplicar(jugador)
    ventana.blit(jugador.image, jugador_rect_cam)

    # HUD
    hud.dibujar(ventana, jugador.vidas)

    pygame.display.flip()