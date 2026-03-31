# nivel1.py
import pygame

ANCHO_NIVEL = 1280
ALTO_NIVEL  = 2800


def cargar_nivel():
    plataformas = [
        pygame.Rect(60,  2550, 220, 28),
        pygame.Rect(280, 2350, 220, 28),
        pygame.Rect(100, 2150, 220, 28),
        pygame.Rect(340, 1940, 220, 28),
        pygame.Rect(160, 1730, 220, 28),
        pygame.Rect(420, 1530, 220, 28),
        pygame.Rect(640, 1330, 220, 28),
        pygame.Rect(420, 1130, 220, 28),
        pygame.Rect(660,  930, 220, 28),
        pygame.Rect(440,  730, 220, 28),
        pygame.Rect(680,  520, 220, 28),
        pygame.Rect(860,  310, 220, 28),
    ]

    suelo     = pygame.Rect(0, 2700, ANCHO_NIVEL, 100)
    zona_meta = pygame.Rect(870, 160, 220, 120)

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
        "titulo"      : "NIVEL 1 - LA CUEVA",
        "numero"      : 1,
    }