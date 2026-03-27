# camera.py
from config import ANCHO, ALTO

class Camera:
    def __init__(self, ancho_nivel, alto_nivel):
        # Guardamos tamaño del nivel
        self.ancho_nivel = ancho_nivel
        self.alto_nivel = alto_nivel

        # Desplazamiento de la cámara
        self.offset_x = 0
        self.offset_y = 0

    def aplicar(self, obj):
        """
        Devuelve un pygame.Rect ajustado por la cámara.
        Acepta:
        - Un objeto que tenga atributo .rect (por ejemplo: jugador)
        - O un pygame.Rect directamente (por ejemplo: una plataforma)
        """
        # Si obj tiene atributo rect (Player u otros sprites), usamos ese rect
        if hasattr(obj, "rect"):
            rect = obj.rect
        else:
            rect = obj  # asumimos que ya es un pygame.Rect

        # devolver una copia desplazada listo para dibujar
        return rect.move(-self.offset_x, -self.offset_y)

    def update(self, jugador):
        """Actualizar offsets para centrar la cámara en el jugador con límites en el nivel."""
        # Queremos centrar la cámara en el jugador (target offsets)
        target_x = jugador.rect.centerx - ANCHO // 2
        target_y = jugador.rect.centery - ALTO // 2

        # Calcular límites máximos (si el nivel es más pequeño que la pantalla -> 0)
        max_x = max(0, self.ancho_nivel - ANCHO)
        max_y = max(0, self.alto_nivel - ALTO)

        # Aplicar clamp para no salirnos del nivel
        self.offset_x = max(0, min(target_x, max_x))
        self.offset_y = max(0, min(target_y, max_y))
