# ver_spritesheet.py  — corre esto UNA sola vez para identificar las filas
import pygame
pygame.init()

SPRITE_W, SPRITE_H = 32, 32   # tamaño de cada frame
COLS, FILAS        = 8, 4     # columnas y filas del spritesheet

ventana = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Identificar filas del spritesheet")
clock   = pygame.time.Clock()
fuente  = pygame.font.SysFont("Arial", 18)

sheet = pygame.image.load("imagenes/frog_green_spritesheet.png").convert_alpha()

frame_actual = 0
fila_actual  = 0
timer        = 0
VELOCIDAD    = 200  # ms por frame

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and fila_actual > 0:
                fila_actual  -= 1
                frame_actual  = 0
            if evento.key == pygame.K_DOWN and fila_actual < FILAS - 1:
                fila_actual  += 1
                frame_actual  = 0

    timer += clock.tick(60)
    if timer >= VELOCIDAD:
        frame_actual = (frame_actual + 1) % COLS
        timer        = 0

    ventana.fill((40, 40, 40))

    # Dibujar frame actual grande (x4)
    frame_rect = pygame.Rect(frame_actual * SPRITE_W, fila_actual * SPRITE_H, SPRITE_W, SPRITE_H)
    frame_surf = sheet.subsurface(frame_rect)
    frame_grande = pygame.transform.scale(frame_surf, (SPRITE_W * 6, SPRITE_H * 6))
    ventana.blit(frame_grande, (220, 160))

    # Dibujar todos los frames de la fila actual pequeños
    for col in range(COLS):
        rect = pygame.Rect(col * SPRITE_W, fila_actual * SPRITE_H, SPRITE_W, SPRITE_H)
        surf = sheet.subsurface(rect)
        surf_grande = pygame.transform.scale(surf, (SPRITE_W * 2, SPRITE_H * 2))
        ventana.blit(surf_grande, (30 + col * 70, 60))
        # Marcar el frame actual
        if col == frame_actual:
            pygame.draw.rect(ventana, (255, 220, 0), (30 + col * 70, 60, SPRITE_W*2, SPRITE_H*2), 2)

    # Textos
    ventana.blit(fuente.render(f"Fila: {fila_actual}  (UP/DOWN para cambiar)", True, (255,255,255)), (30, 20))
    ventana.blit(fuente.render(f"Frame: {frame_actual}/{COLS-1}", True, (200,200,200)), (30, 380))
    ventana.blit(fuente.render("Anota que animacion es cada fila", True, (150,220,100)), (30, 410))

    pygame.display.flip()