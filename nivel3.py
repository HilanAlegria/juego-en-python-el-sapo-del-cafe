# nivel3.py
import pygame

ANCHO_NIVEL = 1280
ALTO_NIVEL  = 3200


def cargar_nivel():

    plataformas = [
        pygame.Rect(60,   2950, 160, 18),  
        pygame.Rect(280,  2750, 160, 18),  
        pygame.Rect(100,  2560, 160, 18),  
        pygame.Rect(380,  2400, 160, 18),  
        pygame.Rect(600,  2250, 160, 18),  
        pygame.Rect(400,  2100, 160, 18), 
        pygame.Rect(720,  1880, 160, 18), 
        pygame.Rect(500,  1680, 160, 18),   
        pygame.Rect(780,  1490, 160, 18),  
        pygame.Rect(520,  1300, 160, 18),   
        pygame.Rect(820,  1110, 160, 18),
        pygame.Rect(540,   920, 160, 18),   
        pygame.Rect(840,   720, 160, 18),   
        pygame.Rect(520,   530, 160, 18),  
        pygame.Rect(780,   320, 160, 18),  
    ]

    suelo     = pygame.Rect(0, 3100, ANCHO_NIVEL, 100)
    zona_meta = pygame.Rect(790, 170, 200, 120)

    return {
        "plataformas" : plataformas,
        "suelo"       : suelo,
        "zona_meta"   : zona_meta,
        "ancho_nivel" : ANCHO_NIVEL,
        "alto_nivel"  : ALTO_NIVEL,
        "tile_plat"   : None,
        "tile_suelo"  : None,
        "capas_fondo" : [],
        "spawn"       : (80, 2880),
        "titulo"      : "NIVEL 3 - LOS ARBOLES",
        "numero"      : 3,
    }