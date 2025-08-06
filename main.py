import mysql.connector
from funciones import *
# Para conectarse a su base de datos, debe ingresar el usuario, password, nombre del servidor, nombre de la base de datos y el puerto.
# Se debe ingresar tanto en main.py como el funciones.py
#conexion = mysql.connector.connect(user="root",password="admin", host="localhost",database="srvp",port=3306)
conexion = mysql.connector.connect(user="root",password="Leonardo", host="127.0.0.1",database="svrp",port=3306)
# print(conexion) 
while True:
    print("=" * 50)
    print("🎮  SRVP - Sistema de Rentas de Videojuegos y PS Plus  🎮".center(50))
    print("=" * 50)
    
    print("\n¿Qué deseas hacer?")
    print("1. Mostrar todos los clientes")
    print("2. Mostrar todas las rentas")
    print("3. Mostrar los videojuegos disponibles")
    print("4. Mostrar las cuentas de playstationPlus disponibles")
    print("5. Mostrar rentas de un cliente")
    print("0. Salir")
    print("-" * 50)

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        mostrar_clientes()
    elif opcion == "2":
        mostrar_rentas()
    elif opcion == "3":
        mostrar_videojuegos()
    elif opcion =="4":
        mostrar_psPlus()
    elif opcion == "5":
        mostrar_rentas_por_cliente()
    elif opcion == "0":
        print("\n👋 ¡Gracias por usar SRVP! Hasta pronto.")
        break
    else:
        print("❌ Opción inválida. Intenta de nuevo.")

    input("\nPresiona Enter para continuar...")
