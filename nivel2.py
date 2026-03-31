# nivel2.py
import pygame

ANCHO_NIVEL = 1280
ALTO_NIVEL  = 2400


def cargar_nivel():
    plataformas = [
        # Plat 1 — inicio izquierda
        pygame.Rect(60,  2150, 220, 28),

        # Plat 2 — Δx=220, Δy=160
        pygame.Rect(280, 1990, 220, 28),

        # Plat 3 — Δx=200, Δy=150 (vuelve izquierda)
        pygame.Rect(120, 1840, 220, 28),

        # Plat 4 — Δx=260, Δy=140
        pygame.Rect(380, 1700, 220, 28),

        # Plat 5 — Δx=200, Δy=140 (vuelve izquierda)
        pygame.Rect(200, 1560, 220, 28),

        # Plat 6 — Δx=260, Δy=130
        pygame.Rect(460, 1430, 220, 28),

        # Plat 7 — Δx=220, Δy=130
        pygame.Rect(660, 1300, 220, 28),

        # Plat 8 — Δx=240, Δy=120 (vuelve izquierda)
        pygame.Rect(440, 1180, 220, 28),

        # Plat 9 — Δx=260, Δy=120
        pygame.Rect(700, 1060, 220, 28),

        # Plat 10 — Δx=240, Δy=120 (vuelve izquierda)
        pygame.Rect(480,  940, 220, 28),

        # Plat 11 — Δx=260, Δy=130
        pygame.Rect(720,  810, 220, 28),

        # Plat 12 — Δx=160, Δy=150
        pygame.Rect(880,  660, 220, 28),

        # Plat 13 — Δx=180, Δy=160 (última antes de meta)
        pygame.Rect(700,  500, 220, 28),
    ]

    suelo     = pygame.Rect(0, 2300, ANCHO_NIVEL, 100)
    pared_izq = pygame.Rect(-40, 0, 40, ALTO_NIVEL)
    pared_der = pygame.Rect(ANCHO_NIVEL, 0, 40, ALTO_NIVEL)
    plataformas += [pared_izq, pared_der]

    zona_meta = pygame.Rect(710, 360, 220, 120)

    return {
        "plataformas" : plataformas,
        "suelo"       : suelo,
        "zona_meta"   : zona_meta,
        "ancho_nivel" : ANCHO_NIVEL,
        "alto_nivel"  : ALTO_NIVEL,
        "tile_plat"   : None,
        "tile_suelo"  : None,
        "capas_fondo" : [],
        "spawn"       : (80, 2080),
        "titulo"      : "NIVEL 2 - LA SUPERFICIE",
        "numero"      : 2,
    }