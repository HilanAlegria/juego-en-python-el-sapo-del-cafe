# nivel1.py
import pygame

ANCHO_NIVEL = 1280
ALTO_NIVEL  = 2400


def cargar_nivel():
    plataformas = [
        # Plat 1 — inicio, esquina inferior izquierda
        pygame.Rect(60,  2150, 220, 28),

        # Plat 2 — Δx=220, Δy=160
        pygame.Rect(280, 1990, 220, 28),

        # Plat 3 — Δx=200, Δy=150 (vuelve izquierda)
        pygame.Rect(120, 1840, 220, 28),

        # Plat 4 — Δx=240, Δy=140
        pygame.Rect(360, 1700, 220, 28),

        # Plat 5 — Δx=200, Δy=140 (vuelve izquierda)
        pygame.Rect(180, 1560, 220, 28),

        # Plat 6 — Δx=240, Δy=140
        pygame.Rect(420, 1420, 220, 28),

        # Plat 7 — Δx=220, Δy=130
        pygame.Rect(640, 1290, 220, 28),

        # Plat 8 — Δx=220, Δy=130 (vuelve izquierda)
        pygame.Rect(420, 1160, 220, 28),

        # Plat 9 — Δx=240, Δy=130
        pygame.Rect(660, 1030, 220, 28),

        # Plat 10 — Δx=220, Δy=130 (vuelve izquierda)
        pygame.Rect(440,  900, 220, 28),

        # Plat 11 — Δx=240, Δy=140
        pygame.Rect(680,  760, 220, 28),

        # Plat 12 — Δx=200, Δy=160 (última antes de la meta)
        pygame.Rect(860,  600, 220, 28),
    ]

    suelo     = pygame.Rect(0, 2300, ANCHO_NIVEL, 100)
    pared_izq = pygame.Rect(-40, 0, 40, ALTO_NIVEL)
    pared_der = pygame.Rect(ANCHO_NIVEL, 0, 40, ALTO_NIVEL)
    plataformas += [pared_izq, pared_der]

    zona_meta = pygame.Rect(870, 460, 220, 120)

    capas_fondo = [
        ("imagenes/parallax-forest-back-trees.png",   0.1),
        ("imagenes/BGBack.png",                       0.15),
        ("imagenes/parallax-forest-lights.png",       0.2),
        ("imagenes/parallax-forest-middle-trees.png", 0.3),
        ("imagenes/CloudsBack.png",                   0.35),
        ("imagenes/BGFront.png",                      0.4),
        ("imagenes/CloudsFront.png",                  0.5),
        ("imagenes/parallax-forest-front-trees.png",  0.6),
    ]

    return {
        "plataformas" : plataformas,
        "suelo"       : suelo,
        "zona_meta"   : zona_meta,
        "ancho_nivel" : ANCHO_NIVEL,
        "alto_nivel"  : ALTO_NIVEL,
        "tile_plat"   : None,
        "tile_suelo"  : None,
        "capas_fondo" : capas_fondo,
        "spawn"       : (80, 2080),
        "titulo"      : "NIVEL 1 - LA CUEVA",
        "numero"      : 1,
    }