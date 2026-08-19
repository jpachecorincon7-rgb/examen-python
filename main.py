import sys
import os
from gestiones.gestion_reparaciones import (
    registrar_reparacion, 
    listar_herramientas_en_reparacion, 
    verificar_actualizaciones_automaticas
)
def mostrar_menu():
    print("\n--- SISTEMA DE CONTROL DE LA JUNTA COMUNAL ---")
    print("1. Ejecutar comando: registrar_reparacion")
    print("2. Ver listado de herramientas en reparación")
    print("3. Salir")
def ejecutar_consola():
    verificar_actualizaciones_automaticas()   
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()  
        if opcion == "1":
            print("\n[Comando registrar_reparacion]")
            id_h = input("Ingrese el ID de la herramienta: ").strip()
            fecha_fin = input("Ingrese fecha estimada de finalización (AAAA-MM-DD): ").strip()
            obs = input("Ingrese observaciones del daño: ").strip()           
            registrar_reparacion(id_h, fecha_fin, obs)           
        elif opcion == "2":
            listar_herramientas_en_reparacion()           
        elif opcion == "3":
            print("Saliendo del sistema de gestión. ¡Feliz día!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
if __name__ == "__main__":
    ejecutar_consola()
