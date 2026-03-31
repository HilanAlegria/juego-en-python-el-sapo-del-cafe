# camera.py
import pygame


class Camera:
    def __init__(self, ancho_nivel, alto_nivel):
        self.ancho_nivel = ancho_nivel
        self.alto_nivel  = alto_nivel
        self.offset_x    = 0.0
        self.offset_y    = 0.0

        # Suavidad: 0.0 = no se mueve, 1.0 = sigue exacto
        # 0.12 da un delay suave pero responsivo
        self.LERP = 0.12

    def aplicar(self, obj):
        if hasattr(obj, "rect"):
            rect = obj.rect
        else:
            rect = obj
        return rect.move(-int(self.offset_x), -int(self.offset_y))

    def update(self, jugador):
        superficie     = pygame.display.get_surface()
        ancho_pantalla = superficie.get_width()
        alto_pantalla  = superficie.get_height()

        # Punto objetivo — centrar al jugador
        target_x = jugador.rect.centerx - ancho_pantalla // 2
        target_y = jugador.rect.centery - alto_pantalla  // 2

        # Clamp al nivel
        max_x = max(0, self.ancho_nivel - ancho_pantalla)
        max_y = max(0, self.alto_nivel  - alto_pantalla)

        target_x = max(0, min(target_x, max_x))
        target_y = max(0, min(target_y, max_y))

        # Lerp — interpola suavemente hacia el objetivo
        self.offset_x += (target_x - self.offset_x) * self.LERP
        self.offset_y += (target_y - self.offset_y) * self.LERP