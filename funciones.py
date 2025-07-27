import time
import mysql.connector
from tabulate import tabulate

def mostrar_menu():
    print("\n¿Qué deseas hacer?")
    print("1️⃣  Mostrar todos los clientes")
    print("2️⃣  Mostrar todas las rentas")
    print("3️⃣  Mostrar los videojuegos disponibles")
    print("0️⃣  Salir")
    print("-" * 50)

def mostrar_rentas():
    print("\n🧾 Rentas Actuales:\n")

    try:
        conexion = mysql.connector.connect(
            user="root",
            password="asdasd",
            host="localhost",
            database="srvp",
            port=3306
        )
        cursor = conexion.cursor()

        # Consulta con JOIN para obtener también el nombre del empleado
        query = """
        SELECT 
            Renta.ID_Renta,
            Empleado.nombre AS Nombre_Empleado,
            Renta.fecha_inicio,
            Renta.fecha_devolucion_esperada,
            Renta.fecha_devolucion_real,
            Renta.estado_renta,
            Renta.hora_transaccion,
            Renta.descuento,
            Renta.Tipo
        FROM Renta
        JOIN Empleado ON Renta.ID_Empleado = Empleado.ID_Empleado
        ORDER BY Renta.ID_Renta;
        """

        cursor.execute(query)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        if resultados:
            print(tabulate(resultados, headers=columnas, tablefmt="fancy_grid"))
        else:
            print("No hay rentas registradas.")

    except mysql.connector.Error as err:
        print("❌ Error al conectar o consultar la base de datos:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()

    time.sleep(1.5)

def mostrar_clientes():
    print("\n👥 Lista de Clientes Registrados:")
    conexion = mysql.connector.connect(
        user="root",
        password="asdasd",
        host="localhost",
        database="srvp",
        port=3306
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Cliente")
    resultados = cursor.fetchall()

    headers = [i[0] for i in cursor.description]  # obtiene los nombres de las columnas
    print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))

    cursor.close()
    conexion.close()
    time.sleep(1.5)

def mostrar_videojuegos():
    print("\n🎲 Videojuegos Disponibles:")
    conexion = mysql.connector.connect(
        user="root",
        password="asdasd",
        host="localhost",
        database="srvp",
        port=3306
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Videojuego WHERE disponibilidad = TRUE")
    resultados = cursor.fetchall()

    headers = [i[0] for i in cursor.description]
    print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))

    cursor.close()
    conexion.close()
    time.sleep(1.5)
