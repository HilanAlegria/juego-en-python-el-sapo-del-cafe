# level.py
import pygame


def cargar_tile(sheet_path, col, fila, tile_size=32, escala=32):
    """Extrae un tile específico de un spritesheet."""
    try:
        sheet = pygame.image.load(sheet_path).convert_alpha()
        rect  = pygame.Rect(col * tile_size, fila * tile_size, tile_size, tile_size)
        tile  = sheet.subsurface(rect)
        return pygame.transform.scale(tile, (escala, escala))
    except Exception as e:
        print(f"Error cargando tile {sheet_path}: {e}")
        return None


def dibujar_plataformas(ventana, platforms, suelo, camera, tile_plat, tile_suelo, color_fallback):
    """Dibuja todas las plataformas y el suelo con textura o color."""
    for plat in platforms:
        rect_cam = camera.aplicar(plat)
        if tile_plat:
            _tiling(ventana, rect_cam, tile_plat)
        else:
            pygame.draw.rect(ventana, color_fallback, rect_cam)

    suelo_cam = camera.aplicar(suelo)
    if tile_suelo:
        _tiling(ventana, suelo_cam, tile_suelo)
    else:
        pygame.draw.rect(ventana, color_fallback, suelo_cam)


def _tiling(ventana, rect, tile):
    """Rellena un rect repitiendo el tile en mosaico."""
    tw = tile.get_width()
    th = tile.get_height()
    for fila in range((rect.height // th) + 2):
        for col in range((rect.width // tw) + 2):
            dest = pygame.Rect(rect.x + col * tw, rect.y + fila * th, tw, th)
            clip = dest.clip(rect)
            if clip.width > 0 and clip.height > 0:
                ventana.blit(tile, clip, pygame.Rect(0, 0, clip.width, clip.height))