# hud.py
import pygame

COLOR_HUD_FONDO = (0, 0, 0, 140)
COLOR_CORAZON   = (220, 50,  50)
COLOR_VACIO     = (60,  60,  60)
COLOR_LABEL     = (180, 255, 180)
COLOR_SCORE     = (255, 220, 50)
COLOR_TIEMPO    = (150, 220, 255)
COLOR_PROGRESO  = (150, 220, 100)

FUENTE = "fuentes/PressStart2P-Regular.ttf"


def dibujar_corazon(ventana, cx, cy, tamanio, color):
    r = tamanio // 2
    pygame.draw.circle(ventana, color, (cx - r // 2, cy - r // 3), r // 2 + 1)
    pygame.draw.circle(ventana, color, (cx + r // 2, cy - r // 3), r // 2 + 1)
    puntos = [
        (cx - r, cy - r // 3),
        (cx + r, cy - r // 3),
        (cx,     cy + r),
    ]
    pygame.draw.polygon(ventana, color, puntos)


class HUD:
    def __init__(self, vidas_max=3):
        self.vidas_max    = vidas_max
        self.fuente_label = pygame.font.Font(FUENTE, 11)
        self.fuente_score = pygame.font.Font(FUENTE, 10)
        self.tamanio_ico  = 22

    def dibujar(self, ventana, vidas, score=0, tiempo=0,
                plat_actual=0, plat_total=0):
        ancho = ventana.get_width()

        # Barra superior
        barra = pygame.Surface((ancho, 52), pygame.SRCALPHA)
        barra.fill(COLOR_HUD_FONDO)
        ventana.blit(barra, (0, 0))

        # --- Vidas (izquierda) ---
        label = self.fuente_label.render("VIDAS", True, COLOR_LABEL)
        ventana.blit(label, (16, 16))

        for i in range(self.vidas_max):
            color = COLOR_CORAZON if i < vidas else COLOR_VACIO
            cx    = 90 + i * (self.tamanio_ico + 10)
            cy    = 26
            dibujar_corazon(ventana, cx, cy, self.tamanio_ico, color)

        # --- Progreso de plataformas (centro) ---
        if plat_total > 0:
            texto_prog = f"{plat_actual}/{plat_total}"
            prog = self.fuente_score.render(texto_prog, True, COLOR_PROGRESO)
            ventana.blit(prog, prog.get_rect(center=(ancho // 2, 26)))

        # --- Score y tiempo (derecha) ---
        mins  = tiempo // 60
        segs  = tiempo % 60
        texto_tiempo = f"{mins:02d}:{segs:02d}"
        texto_score  = f"SCORE {score:06d}"

        t_surf = self.fuente_score.render(texto_tiempo, True, COLOR_TIEMPO)
        s_surf = self.fuente_score.render(texto_score,  True, COLOR_SCORE)

        ventana.blit(t_surf, t_surf.get_rect(topright=(ancho - 16, 8)))
        ventana.blit(s_surf, s_surf.get_rect(topright=(ancho - 16, 30)))