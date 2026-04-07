# nivel2.py
import pygame

ANCHO_NIVEL = 1280
ALTO_NIVEL  = 3400


def cargar_nivel():
    # Montaña rusa real — bajadas de 280-320px, subidas de 280-350px
    # Separación horizontal mínima 240px entre plataformas consecutivas
    # Ninguna plataforma comparte rango X con la inmediatamente anterior
    plataformas = [
        # --- Zona baja ---
        pygame.Rect(60,  3150, 240, 28),   # 1  spawn — izquierda
        pygame.Rect(360, 2850, 220, 28),   # 2  SUBE 300 — centro-izquierda
        pygame.Rect(80,  3150, 200, 28),   # 3  BAJA 300 — izquierda
        pygame.Rect(380, 2820, 220, 28),   # 4  SUBE 330 — centro
        pygame.Rect(700, 3120, 200, 28),   # 5  BAJA 300 — derecha

        # --- Zona media-baja ---
        pygame.Rect(420, 2780, 220, 28),   # 6  SUBE 340 — centro
        pygame.Rect(740, 3060, 200, 28),   # 7  BAJA 280 — derecha
        pygame.Rect(460, 2740, 220, 28),   # 8  SUBE 320 — centro-izquierda

        # --- Zona media ---
        pygame.Rect(760, 3020, 200, 28),   # 9  BAJA 280 — derecha
        pygame.Rect(480, 2680, 220, 28),   # 10 SUBE 340 — centro
        pygame.Rect(780, 2380, 220, 28),   # 11 SUBE 300 — derecha

        # --- Zona alta ---
        pygame.Rect(500, 2100, 220, 28),   # 12 SUBE 280 — centro vuelve izq
        pygame.Rect(780, 1800, 220, 28),   # 13 SUBE 300 — derecha
        pygame.Rect(500, 1500, 220, 28),   # 14 SUBE 300 — izquierda
    ]

    suelo     = pygame.Rect(0, 3300, ANCHO_NIVEL, 100)
    zona_meta = pygame.Rect(510, 1350, 220, 120)

    return {
        "plataformas" : plataformas,
        "suelo"       : suelo,
        "zona_meta"   : zona_meta,
        "ancho_nivel" : ANCHO_NIVEL,
        "alto_nivel"  : ALTO_NIVEL,
        "tile_plat"   : None,
        "tile_suelo"  : None,
        "capas_fondo" : [],
        "spawn"       : (80, 3080),
        "titulo"      : "NIVEL 2 - LA SUPERFICIE",
        "numero"      : 2,
    }