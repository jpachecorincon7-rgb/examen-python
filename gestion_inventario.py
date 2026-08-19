import json
import os

INVENTARIO_PATH = "inventario.json"

def cargar_inventario():
    # Datos de prueba iniciales si el archivo no existe
    if not os.path.exists(INVENTARIO_PATH):
        datos_iniciales = {
            "1": {"nombre": "Cortadora de césped", "estado": "Activa"},
            "2": {"nombre": "Taladro percutor", "estado": "Activa"},
            "3": {"nombre": "Motosierra", "estado": "En reparación"}
        }
        with open(INVENTARIO_PATH, 'w', encoding='utf-8') as f:
            json.dump(datos_iniciales, f, indent=4, ensure_ascii=False)
        return datos_iniciales
    
    with open(INVENTARIO_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_inventario(inventario):
    with open(INVENTARIO_PATH, 'w', encoding='utf-8') as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)
