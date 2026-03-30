# level.py
import pygame

def cargar_nivel1():
    plataformas = [
        pygame.Rect(0,   1950, 1280, 50),  
        pygame.Rect(100, 1750,  300, 30),
        pygame.Rect(500, 1550,  300, 30),
        pygame.Rect(200, 1350,  300, 30),
        pygame.Rect(600, 1150,  300, 30),
        pygame.Rect(300,  950,  300, 30),
        pygame.Rect(700,  750,  300, 30),
        pygame.Rect(400,  550,  300, 30),
        pygame.Rect(200,  350,  300, 30),
        pygame.Rect(600,  200,  300, 30),   
    ]


    zona_meta = pygame.Rect(650, 100, 200, 90)

    return plataformas, zona_meta, 1280, 2000