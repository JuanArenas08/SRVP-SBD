import mysql.connector
from conexion import *
from tabulate import tabulate
import time
#CONECTAMOS A LA BASE DE DATOS

#def conectar():
#    return mysql.connector.connect(
#        user="root",
#        password="admin",
#        host="hostname",
#        database="srvp",
#        port=3306
#    )

#CRUD CLIENTE
#AÑADIR

def agregar_cliente(id_cliente, email, historial, nombre_completo, telefono):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Cliente (ID_Cliente, email, historial, nombre_completo, telefono)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (id_cliente, email, historial, nombre_completo, telefono)
        cursor.execute(sql, valores)
        conn.commit()
        print("✅ Cliente agregado exitosamente.")
    except mysql.connector.Error as err:
        print(f"❌ No se ha podido agregar el cliente nuevo - Ingresar nuevamente con datos válidos. Error: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

#CONSULTAR
'''
def mostrar_clientes():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cliente")
        resultados = cursor.fetchall()
        for cliente in resultados:
            print(cliente)
    except mysql.connector.Error as err:
        print(f"❌ Error al mostrar clientes. Detalles: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
'''




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

#EDITAR

def actualizar_cliente(id_cliente, email, historial, nombre_completo, telefono):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = """
        UPDATE Cliente
        SET email = %s,
            historial = %s,
            nombre_completo = %s,
            telefono = %s
        WHERE ID_Cliente = %s
        """
        valores = (email, historial, nombre_completo, telefono, id_cliente)
        cursor.execute(sql, valores)
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Cliente actualizado exitosamente.")
        else:
            print("⚠️ No se encontró un cliente con ese ID.")
    except mysql.connector.Error as err:
        print(f"❌ No se ha podido actualizar el cliente - Ingresar nuevamente con datos válidos. Error: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

#ELIMINAR

def eliminar_cliente(id_cliente):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "DELETE FROM Cliente WHERE ID_Cliente = %s"
        cursor.execute(sql, (id_cliente,))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Cliente eliminado exitosamente.")
        else:
            print("⚠️ No se encontró un cliente con ese ID.")
    except mysql.connector.Error as err:
        print(f"❌ No se ha podido eliminar el cliente - Ingresar nuevamente con datos válidos. Error: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()



# CRUD RENTAS


#
def mostrar_rentas():
    print("\n🧾 Rentas Actuales:\n")

    try:
        conexion = obtener_conexion() 
        cursor = conexion.cursor()

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


def id_cliente_existe(id_cliente):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Cliente FROM Cliente WHERE ID_Cliente = %s", (id_cliente,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"❌ Error al verificar ID: {err}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


# CRUD Empleados

# Agregar empleado
def crear_empleado():
    print("\n👤 Agregar nuevo empleado:")

    try:
        id_empleado = input("ID del empleado (ej: 12): ").strip()
        nombre = input("Nombre del empleado (ej: Leonardo Cardoso): ").strip()
        rol = input("Rol del empleado (ej: Vendedor): ").strip()

        # Validación básica
        if not id_empleado.isdigit():
            print("❌ El ID debe ser un número.")
            return
        if not nombre or not rol:
            print("❌ Nombre y rol son obligatorios.")
            return

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si el ID ya existe
        cursor.execute("SELECT * FROM Empleado WHERE ID_Empleado = %s", (id_empleado,))
        if cursor.fetchone():
            print("⚠️ Ya existe un empleado con ese ID.")
            return

        query = "INSERT INTO Empleado (ID_Empleado, nombre, rol) VALUES (%s, %s, %s)"
        cursor.execute(query, (int(id_empleado), nombre, rol))
        conexion.commit()

        print("✅ Empleado agregado exitosamente.")

        cursor.execute("SELECT * FROM Empleado")
        print(tabulate(cursor.fetchall(), headers=[desc[0] for desc in cursor.description], tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print("❌ Error al agregar el empleado:", err)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()


# Mostrar empleados

def mostrar_empleados():
    print("\n📋 Lista de empleados:")
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Empleado")
        print(tabulate(cursor.fetchall(), headers=[desc[0] for desc in cursor.description], tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print("❌ Error al consultar empleados:", err)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

# Editar empleado

def editar_empleado():
    print("\n✏️ Editar empleado:")
    nombre = input("Ingrese el nombre del empleado a editar: ").strip()

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM Empleado WHERE nombre = %s", (nombre,))
        empleado = cursor.fetchone()

        if not empleado:
            print("❌ Empleado no encontrado.")
            return

        print(tabulate([empleado], headers=[desc[0] for desc in cursor.description], tablefmt="fancy_grid"))

        nuevo_nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ").strip()
        nuevo_rol = input("Nuevo rol (dejar en blanco para no cambiar): ").strip()

        campos = []
        valores = []

        if nuevo_nombre:
            campos.append("nombre = %s")
            valores.append(nuevo_nombre)
        if nuevo_rol:
            campos.append("rol = %s")
            valores.append(nuevo_rol)

        if not campos:
            print("⚠️ No se realizaron cambios.")
            return

        valores.append(nombre)  # Para el WHERE
        query = f"UPDATE Empleado SET {', '.join(campos)} WHERE nombre = %s"
        cursor.execute(query, tuple(valores))
        conexion.commit()

        print("✅ Empleado actualizado.")
        cursor.execute("SELECT * FROM Empleado")
        print(tabulate(cursor.fetchall(), headers=[desc[0] for desc in cursor.description], tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print("❌ Error al editar empleado:", err)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()


# Eliminar empleado

def eliminar_empleado():
    print("\n🗑️ Eliminar empleado:")
    nombre = input("Ingrese el nombre del empleado a eliminar: ").strip()

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM Empleado WHERE nombre = %s", (nombre,))
        empleado = cursor.fetchone()

        if not empleado:
            print("❌ Empleado no encontrado.")
            return

        print(tabulate([empleado], headers=[desc[0] for desc in cursor.description], tablefmt="fancy_grid"))

        confirmar = input("¿Está seguro que desea eliminar este empleado? (s/n): ").strip().lower()
        if confirmar != "s":
            print("❌ Operación cancelada.")
            return

        cursor.execute("DELETE FROM Empleado WHERE nombre = %s", (nombre,))
        conexion.commit()

        print("✅ Empleado eliminado.")
        cursor.execute("SELECT * FROM Empleado")
        print(tabulate(cursor.fetchall(), headers=[desc[0] for desc in cursor.description], tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print("❌ Error al eliminar empleado:", err)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()