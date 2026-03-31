# progreso.py
import json
import os

ARCHIVO = "progreso.json"


def cargar_progreso():
    """Carga el progreso guardado. Si no existe, solo nivel 1 desbloqueado."""
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r") as f:
                datos = json.load(f)
                return datos.get("niveles_desbloqueados", 1)
        except:
            return 1
    return 1


def guardar_progreso(niveles_desbloqueados):
    """Guarda cuántos niveles están desbloqueados."""
    try:
        with open(ARCHIVO, "w") as f:
            json.dump({"niveles_desbloqueados": niveles_desbloqueados}, f)
    except Exception as e:
        print(f"Error guardando progreso: {e}")


def desbloquear_siguiente(nivel_actual, total_niveles):
    """
    Desbloquea el siguiente nivel si corresponde.
    Retorna el nuevo total de niveles desbloqueados.
    """
    desbloqueados = cargar_progreso()
    # Solo desbloquea si completó el último nivel desbloqueado
    if nivel_actual + 1 >= desbloqueados and nivel_actual + 1 < total_niveles:
        desbloqueados = nivel_actual + 2  # +2 porque es índice base 0
        guardar_progreso(desbloqueados)
    return desbloqueados