import mysql.connector
from funciones import *
from conexion import *
# Para conectarse a su base de datos, debe ingresar el usuario, password, nombre del servidor, nombre de la base de datos y el puerto.
# Se debe ingresar tanto en main.py como el funciones.py

# MENÚ PRINCIPAL
while True:
    print("=" * 50)
    print("🎮  SRVP - Sistema de Rentas de Videojuegos y PS Plus  🎮".center(50))
    print("=" * 50)
    
    print("\n¿Qué deseas hacer?")
    print("1. Administrar Clientes")
    print("2. Administrar Rentas")
    print("3. Administrar empleados")
    print("4. Mostrar las cuentas de playstationPlus disponibles")
    print("5. Administrar Transacciones")
    print("6. Administrar Multas")
    print("0. Salir")
    print("-" * 50)

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        clientes()
    elif opcion == "2":
        rentas()
    elif opcion == "3":
        menu_administrar_empleados()
    elif opcion =="4":
        mostrar_psPlus()
    elif opcion == "5":
        transacciones()
    elif opcion == "6":
        multas()
    elif opcion == "0":
        print("\n👋 ¡Gracias por usar SRVP! Hasta pronto.")
        break
    else:
        print("❌ Opción inválida. Intenta de nuevo.")

    input("\nPresiona Enter para continuar...")
