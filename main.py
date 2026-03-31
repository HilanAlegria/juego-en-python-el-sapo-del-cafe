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
#  Score                                                               #
# ------------------------------------------------------------------ #
PUNTOS_BASE      = 1000
PUNTOS_POR_VIDA  = 200
PUNTOS_POR_SEG   = 5     # se restan por cada segundo
MULTIPLICADORES  = [1.0, 1.5, 2.0]  # x nivel


def calcular_score(vidas, tiempo_seg, num_nivel):
    base   = PUNTOS_BASE
    bonus  = vidas * PUNTOS_POR_VIDA
    penali = tiempo_seg * PUNTOS_POR_SEG
    total  = max(100, int((base + bonus - penali) * MULTIPLICADORES[num_nivel]))
    return total


# ------------------------------------------------------------------ #
#  Flash de pantalla al perder vida                                    #
# ------------------------------------------------------------------ #
flash_timer  = 0
FLASH_DURACION = 12  # frames


def activar_flash():
    global flash_timer
    flash_timer = FLASH_DURACION


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

# Variables de sesión
tiempo_inicio   = pygame.time.get_ticks()
vidas_previas   = jugador.vidas

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
                tiempo_inicio = pygame.time.get_ticks()
                vidas_previas = jugador.vidas

    teclas = pygame.key.get_pressed()

    platforms        = datos["plataformas"]
    suelo            = datos["suelo"]
    zona_meta        = datos["zona_meta"]
    ancho_nivel      = datos["ancho_nivel"]
    alto_nivel       = datos["alto_nivel"]
    spawn_x, spawn_y = datos["spawn"]

    # --- Lógica ---
    jugador.handle_input(teclas)
    jugador.jump(teclas)
    jugador.apply_gravity()
    jugador.move([*platforms, suelo], alto_nivel)
    jugador.update(dt)

    # Clamp horizontal
    jugador.rect.left  = max(0, jugador.rect.left)
    jugador.rect.right = min(ancho_nivel, jugador.rect.right)

    # Detectar pérdida de vida para activar flash
    if jugador.vidas < vidas_previas:
        activar_flash()
    vidas_previas = jugador.vidas

    # Caída fuera del nivel
    if jugador.rect.top > alto_nivel:
        jugador.perder_vida(spawn_x, spawn_y)
        activar_flash()

    # Caída fatal
    if jugador._caida_fatal:
        jugador.perder_vida(spawn_x, spawn_y)
        jugador._caida_fatal = False
        activar_flash()

    # Tiempo transcurrido en segundos
    tiempo_seg = (pygame.time.get_ticks() - tiempo_inicio) // 1000

    # Progreso de plataformas — contar cuántas está por encima el jugador
    plats_superadas = sum(
        1 for p in platforms
        if jugador.rect.top < p.top
    )

    # Forma más simple y correcta de contar progreso
    plats_normales  = [p for p in platforms
                       if p.width < ancho_nivel and p.height < 80]
    plat_total      = len(plats_normales)
    plat_actual     = sum(1 for p in plats_normales if jugador.rect.top < p.top)

    # --- Victoria ---
    if jugador.rect.colliderect(zona_meta):
        desbloquear_siguiente(nivel_actual, len(NIVELES))
        score_final = calcular_score(jugador.vidas, tiempo_seg, nivel_actual)

        captura    = ventana.copy()
        pantalla_v = PantallaVictoria(ventana, captura, jugador.vidas)
        pantalla_v.score_final = score_final
        resultado  = pantalla_v.ejecutar()

        if resultado == "siguiente":
            if nivel_actual < len(NIVELES) - 1:
                vidas_ant    = jugador.vidas
                nivel_actual += 1
                datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)
                jugador.vidas  = vidas_ant
                tiempo_inicio  = pygame.time.get_ticks()
                vidas_previas  = jugador.vidas
            else:
                mostrar_menu()
                nivel_actual = 0
                datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)
                tiempo_inicio = pygame.time.get_ticks()
                vidas_previas = jugador.vidas
        elif resultado == "menu":
            mostrar_menu()
            datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)
            tiempo_inicio = pygame.time.get_ticks()
            vidas_previas = jugador.vidas

    # --- Game Over ---
    if jugador.esta_muerto():
        captura     = ventana.copy()
        pantalla_go = PantallaGameOver(ventana, captura)
        resultado   = pantalla_go.ejecutar()

        if resultado == "reintentar":
            datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)
            tiempo_inicio = pygame.time.get_ticks()
            vidas_previas = jugador.vidas
        elif resultado == "menu":
            mostrar_menu()
            datos, jugador, camera = iniciar_juego(sapo_path, nivel_actual)
            tiempo_inicio = pygame.time.get_ticks()
            vidas_previas = jugador.vidas

    # --- Cámara ---
    camera.update(jugador)

    # --- Dibujo ---
    ventana.fill((10, 10, 10))

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

    # Jugador — centrar imagen con squash/stretch
    jugador_rect_cam = camera.aplicar(jugador)
    img_rect         = jugador.image.get_rect(center=jugador_rect_cam.center)
    ventana.blit(jugador.image, img_rect)

    # Flash rojo al perder vida
    if flash_timer > 0:
        flash_timer -= 1
        alpha     = int(160 * (flash_timer / FLASH_DURACION))
        flash_surf = pygame.Surface(ventana.get_size(), pygame.SRCALPHA)
        flash_surf.fill((220, 0, 0, alpha))
        ventana.blit(flash_surf, (0, 0))

    # HUD
    hud.dibujar(
        ventana,
        jugador.vidas,
        score=calcular_score(jugador.vidas, tiempo_seg, nivel_actual),
        tiempo=tiempo_seg,
        plat_actual=plat_actual,
        plat_total=plat_total
    )

    pygame.display.flip()