import mysql.connector
from funciones import *
from conexion import *
# Para conectarse a su base de datos, debe ingresar el usuario, password, nombre del servidor, nombre de la base de datos y el puerto.
# Se debe ingresar en conexion.py
# MENÚ PRINCIPAL
while True:
    print("=" * 50)
    print("🎮  SRVP - Sistema de Rentas de Videojuegos y PS Plus  🎮".center(50))
    print("=" * 50)
    
    print("\n¿Qué deseas hacer?")
    print("1. Administrar Clientes")
    print("2. Administrar Rentas")
    print("3. Administrar empleados")
    print("4. Administrar Transacciones")
    print("5. Administrar Multas")
    print("6. Administrar Método de Pago")
    print("7. Reportes y Estadísticas")
    print("0. Salir")
    print("-" * 50)

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        clientes()
    elif opcion == "2":
        rentas()
    elif opcion == "3":
        menu_administrar_empleados()
    elif opcion == "4":
        transacciones()
    elif opcion == "5":
        multas()
    elif opcion == "6":
        metodo_pago()

    elif opcion == "7":
        menu_reportes()
    elif opcion == "0":
        print("\n👋 ¡Gracias por usar SRVP! Hasta pronto.")
        break
    else:
        print("❌ Opción inválida. Intenta de nuevo.")

    input("\nPresiona Enter para continuar...")
