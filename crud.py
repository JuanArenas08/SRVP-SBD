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
