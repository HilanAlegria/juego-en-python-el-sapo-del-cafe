# nivel2.py
import pygame

ANCHO_NIVEL = 1280
ALTO_NIVEL  = 2800


def cargar_nivel():
    plataformas = [

        pygame.Rect(60,   2550, 240, 28),  # 1 spawn
        pygame.Rect(340,  2280, 200, 28),  # 2 Δy=270
        pygame.Rect(160,  2400, 200, 28),  # 3 Δy=-120 baja
        pygame.Rect(420,  2080, 220, 28),  # 4 Δy=320
        pygame.Rect(680,  2260, 200, 28),  # 5 Δy=-180 baja
        pygame.Rect(460,  1900, 220, 28),  # 6 Δy=360
        pygame.Rect(720,  2020, 200, 28),  # 7 Δy=-120 baja
        pygame.Rect(940,  1760, 200, 28),  # 8 Δy=260
        pygame.Rect(680,  1880, 220, 28),  # 9 Δy=-120 baja
        pygame.Rect(420,  1580, 220, 28),  # 10 Δy=300
        pygame.Rect(680,  1340, 220, 28),  # 11 Δy=240
        pygame.Rect(900,  1460, 200, 28),  # 12 Δy=-120 baja
        pygame.Rect(580,  1140, 220, 28),  # 13 Δy=320
        pygame.Rect(820,   880, 220, 28),  # 14 Δy=260
    ]

    suelo     = pygame.Rect(0, 2700, ANCHO_NIVEL, 100)
    zona_meta = pygame.Rect(830, 730, 220, 120)

    return {
        "plataformas" : plataformas,
        "suelo"       : suelo,
        "zona_meta"   : zona_meta,
        "ancho_nivel" : ANCHO_NIVEL,
        "alto_nivel"  : ALTO_NIVEL,
        "tile_plat"   : None,
        "tile_suelo"  : None,
        "capas_fondo" : [],
        "spawn"       : (80, 2480),
        "titulo"      : "NIVEL 2 - LA SUPERFICIE",
        "numero"      : 2,
    }