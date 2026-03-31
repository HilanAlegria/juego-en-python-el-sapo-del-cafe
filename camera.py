# camera.py
import pygame


class Camera:
    def __init__(self, ancho_nivel, alto_nivel):
        self.ancho_nivel = ancho_nivel
        self.alto_nivel  = alto_nivel
        self.offset_x    = 0
        self.offset_y    = 0

    def aplicar(self, obj):
        if hasattr(obj, "rect"):
            rect = obj.rect
        else:
            rect = obj
        return rect.move(-self.offset_x, -self.offset_y)

    def update(self, jugador):
        # Usar tamaño real de la ventana en lugar de constantes
        ventana_info = pygame.display.get_surface()
        ancho_pantalla = ventana_info.get_width()
        alto_pantalla  = ventana_info.get_height()

        target_x = jugador.rect.centerx - ancho_pantalla // 2
        target_y = jugador.rect.centery - alto_pantalla  // 2

        max_x = max(0, self.ancho_nivel - ancho_pantalla)
        max_y = max(0, self.alto_nivel  - alto_pantalla)

        self.offset_x = max(0, min(target_x, max_x))
        self.offset_y = max(0, min(target_y, max_y))