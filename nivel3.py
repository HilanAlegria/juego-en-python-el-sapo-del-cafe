# nivel3.py
import pygame

ANCHO_NIVEL = 1280
ALTO_NIVEL  = 2400


def cargar_nivel():
    plataformas = [
        # Plat 1 — inicio izquierda (ramas más angostas)
        pygame.Rect(60,  2150, 180, 20),

        # Plat 2 — Δx=200, Δy=150
        pygame.Rect(260, 2000, 180, 20),

        # Plat 3 — Δx=180, Δy=140 (vuelve izquierda)
        pygame.Rect(100, 1860, 180, 20),

        # Plat 4 — Δx=240, Δy=140
        pygame.Rect(340, 1720, 180, 20),

        # Plat 5 — Δx=200, Δy=130 (vuelve izquierda)
        pygame.Rect(160, 1590, 180, 20),

        # Plat 6 — Δx=260, Δy=130
        pygame.Rect(420, 1460, 180, 20),

        # Plat 7 — Δx=240, Δy=120
        pygame.Rect(660, 1340, 180, 20),

        # Plat 8 — Δx=220, Δy=120 (vuelve izquierda)
        pygame.Rect(440, 1220, 180, 20),

        # Plat 9 — Δx=260, Δy=120
        pygame.Rect(700, 1100, 180, 20),

        # Plat 10 — Δx=240, Δy=120 (vuelve izquierda)
        pygame.Rect(460,  980, 180, 20),

        # Plat 11 — Δx=260, Δy=130
        pygame.Rect(720,  850, 180, 20),

        # Plat 12 — Δx=200, Δy=140 (vuelve izquierda)
        pygame.Rect(520,  710, 180, 20),

        # Plat 13 — Δx=240, Δy=150
        pygame.Rect(760,  560, 180, 20),

        # Plat 14 — Δx=180, Δy=160 (última, más difícil)
        pygame.Rect(580,  400, 180, 20),
    ]

    suelo     = pygame.Rect(0, 2300, ANCHO_NIVEL, 100)
    pared_izq = pygame.Rect(-40, 0, 40, ALTO_NIVEL)
    pared_der = pygame.Rect(ANCHO_NIVEL, 0, 40, ALTO_NIVEL)
    plataformas += [pared_izq, pared_der]

    zona_meta = pygame.Rect(590, 260, 220, 120)

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
        "titulo"      : "NIVEL 3 - LOS ARBOLES",
        "numero"      : 3,
    }
