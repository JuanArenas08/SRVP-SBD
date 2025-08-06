
from crud import *


def obtener_conexion():
    return mysql.connector.connect(
        user="root",        # ingrese nombre del usuario
        password="asdasd",   # ingrese contraseña de su servidor
        host="localhost",   # ingrese nombre del servidor
        database="srvp",    # ingrese nombre de la base de datos
        port=3306           # ingrse el puerto, por defecto es el 3306
    )

def mostrar_menu():
    print("\n¿Qué deseas hacer?")
    print("1️⃣  Mostrar todos los clientes")
    print("2️⃣  Mostrar todas las rentas")
    print("3️⃣  Mostrar los videojuegos disponibles")
    print("0️⃣  Salir")
    print("-" * 50)


def rentas():
    while True:
        print("\n¿Qué deseas hacer en Rentas?")
        print("1️⃣  Añadir Rentas")
        print("2️⃣  Mostrar todas las rentas")
        print("3️⃣  Editar Rentas Existentes")
        print("4️⃣  Eliminar Rentas Existentes")
        print("0️⃣  Salir")
        print("-" * 50)

        opc = input ("Seleccione una opción: ")
        if opc == "1":
            print("asd")
        elif opc == "2":
            mostrar_rentas()
        elif opc == "3":
            mostrar_rentas
        elif opc == "4":
            mostrar_rentas
        elif opc == "0":
            print("Saliendo del menú de Rentas...")
            break
        else:
            print("Opción no válida. Intente nuevamente...")
        



def mostrar_clientes():
    print("\n👥 Lista de Clientes Registrados:")
    try:
        conexion = obtener_conexion()  # ✅
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Cliente")
        resultados = cursor.fetchall()

        headers = [i[0] for i in cursor.description]
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print("❌ Error:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()

    time.sleep(1.5)

def mostrar_videojuegos():
    print("\n🎲 Videojuegos Disponibles:")
    try:
        conexion = obtener_conexion()  # ✅
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Videojuego WHERE disponibilidad = TRUE")
        resultados = cursor.fetchall()

        headers = [i[0] for i in cursor.description]
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print("❌ Error:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()

    time.sleep(1.5)

def mostrar_psPlus():
    print("\n🔐 Cuentas PS Plus Disponibles:")
    try:
        conexion = obtener_conexion()  # ✅
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM PS_PLUS WHERE disponibilidad = TRUE")
        resultados = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print("❌ Error:", err)
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()

    time.sleep(1.5)  

def mostrar_rentas_por_cliente():
    print("\n📄 Consultar Rentas por Cliente:")
    try:
        id_cliente = input("Ingrese el ID del cliente: ").strip()

        if not id_cliente.isdigit():
            print("⚠️ El ID debe ser un número válido.")
            return

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        query = """
        SELECT 
            c.ID_Cliente,
            c.nombre_completo,
            r.ID_Renta,
            r.fecha_inicio,
            r.fecha_devolucion_esperada,
            r.fecha_devolucion_real,
            r.estado_renta,
            r.Tipo AS tipo_renta,
            e.nombre AS empleado_asignado
        FROM Cliente c
        JOIN REALIZA rel ON c.ID_Cliente = rel.ID_Cliente
        JOIN Renta r ON rel.ID_Renta = r.ID_Renta
        JOIN Empleado e ON r.ID_Empleado = e.ID_Empleado
        WHERE c.ID_Cliente = %s
        ORDER BY r.fecha_inicio DESC;
        """
        cursor.execute(query, (id_cliente,))
        resultados = cursor.fetchall()

        if resultados:
            headers = [desc[0] for desc in cursor.description]
            print(f"\n🧾 Rentas del cliente {resultados[0][1]}:")
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("ℹ️ Este cliente no tiene rentas registradas.")

    except mysql.connector.Error as err:
        print("❌ Error al consultar la base de datos:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()

    time.sleep(1.5)


