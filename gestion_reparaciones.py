import os
import json
from datetime import datetime
from gestiones.gestion_inventario import cargar_inventario, guardar_inventario
REPARACIONES_PATH = os.path.join("reports", "reparaciones.json")
def inicializar_archivo_reparaciones():
    """Asegura que exista la carpeta reports y el archivo json vacío si no existen."""
    if not os.path.exists("reports"):
        os.makedirs("reports")
    if not os.path.exists(REPARACIONES_PATH):
        with open(REPARACIONES_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4, ensure_ascii=False)
def listar_herramientas_en_reparacion():
    """Muestra en consola el listado actual de reparaciones."""
    inicializar_archivo_reparaciones()
    with open(REPARACIONES_PATH, 'r', encoding='utf-8') as f:
        reparaciones = json.load(f)    
    print("\n=== HERRAMIENTAS EN REPARACIÓN ===")
    if not reparaciones:
        print("No hay herramientas registradas en reparación actualmente.")
        return        
    for rep in reparaciones:
        print(f"ID: {rep['id_herramienta']} | Nombre: {rep['nombre']}")
        print(f"   Inicio: {rep['fecha_inicio']} | Est. Fin: {rep['fecha_estimada_fin']}")
        print(f"   Observaciones: {rep['observaciones']}")
        print("-" * 40)
def verificar_actualizaciones_automaticas():
    """Cambia automáticamente a 'Activa' si ya llegó o pasó la fecha estimada."""
    inventario = cargar_inventario()
    inicializar_archivo_reparaciones()    
    with open(REPARACIONES_PATH, 'r', encoding='utf-8') as f:
        reparaciones = json.load(f)    
    fecha_actual = datetime.now().date()
    reparaciones_activas = []
    cambios_realizados = False
    for rep in reparaciones:
        fecha_fin = datetime.strptime(rep['fecha_estimada_fin'], "%Y-%m-%d").date()        
        if fecha_actual >= fecha_fin:
            id_h = rep['id_herramienta']
            if id_h in inventario:
                inventario[id_h]['estado'] = "Activa"
                print(f"\n[AUTO] ¡Reparación finalizada! ID {id_h} ({rep['nombre']}) vuelve a estar 'Activa'.")
                cambios_realizados = True
        else:
            reparaciones_activas.append(rep)
    if cambios_realizados:
        guardar_inventario(inventario)
        with open(REPARACIONES_PATH, 'w', encoding='utf-8') as f:
            json.dump(reparaciones_activas, f, indent=4, ensure_ascii=False)
def registrar_reparacion(id_herramienta, fecha_estimada_fin, observaciones):
    """Registra la reparación. Si la herramienta no existe, la crea desde cero."""
    inventario = cargar_inventario()
    inicializar_archivo_reparaciones()
    if id_herramienta not in inventario:
        print(f"\n[NUEVA HERRAMIENTA] El ID '{id_herramienta}' no existe en el inventario.")
        nombre_nuevo = input("→ Ingrese el NOMBRE para registrar esta herramienta desde cero: ").strip()
        if not nombre_nuevo:
            print("Error: El nombre de la herramienta no puede estar vacío. Registro cancelado.")
            return
        inventario[id_herramienta] = {
            "nombre": nombre_nuevo,
            "estado": "Activa"
        }
        guardar_inventario(inventario)
        print(f"✓ Herramienta '{nombre_nuevo}' añadida correctamente al inventario base.")
    herramienta = inventario[id_herramienta]
    if herramienta['estado'] == "En reparación":
        print(f"\nAdvertencia: La herramienta '{herramienta['nombre']}' ya está en estado 'En reparación'.")
        return
    try:
        datetime.strptime(fecha_estimada_fin, "%Y-%m-%d")
    except ValueError:
        print("\nError: Formato de fecha inválido. Utilice AAAA-MM-DD (Ej: 2026-08-30).")
        return
    herramienta['estado'] = "En reparación"
    guardar_inventario(inventario)
    fecha_inicio = datetime.now().strftime("%Y-%m-%d")
    nuevo_registro = {
        "id_herramienta": id_herramienta,
        "nombre": herramienta['nombre'],
        "fecha_inicio": fecha_inicio,
        "fecha_estimada_fin": fecha_estimada_fin,
        "observaciones": observaciones
    }
    with open(REPARACIONES_PATH, 'r', encoding='utf-8') as f:
        reparaciones = json.load(f)
    reparaciones.append(nuevo_registro)
    with open(REPARACIONES_PATH, 'w', encoding='utf-8') as f:
        json.dump(reparaciones, f, indent=4, ensure_ascii=False)
    print(f"\nÉxito: '{herramienta['nombre']}' (ID: {id_herramienta}) ha sido puesta en reparación.")