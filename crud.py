import mysql.connector
from conexion import *
from tabulate import tabulate
from datetime import datetime
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



# CRUD RENTAS
def id_existe(tabla, columna, valor):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        query = f"SELECT {columna} FROM {tabla} WHERE {columna} = %s"
        cursor.execute(query, (valor,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"❌ Error al verificar {tabla}: {err}")
        return False
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

#AGREGAR RENTA

def agregar_renta(id_renta, id_empleado, fecha_inicio,
                  fecha_devolucion_real, fecha_devolucion_esperada,
                  estado_renta, hora_transaccion, tipo, descuento=0):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO Renta (ID_Renta, ID_Empleado, Fecha_Inicio, "
            "Fecha_Devolucion_Real, Fecha_Devolucion_Esperada, Estado_Renta, "
            "Hora_Transaccion, Tipo, Descuento) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (id_renta, id_empleado, fecha_inicio,
             fecha_devolucion_real, fecha_devolucion_esperada,
             estado_renta, hora_transaccion, tipo, descuento)
        )
        conexion.commit()
        print("✅ Renta agregada exitosamente.")
    except mysql.connector.Error as error:
        print(f"❌ Error al agregar la renta: {error}")
    finally:
        cursor.close()
        conexion.close()


#ELIMINAR RENTA

def eliminar_renta(id_renta):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "DELETE FROM Renta WHERE ID_Renta = %s"
        cursor.execute(sql, (id_renta,))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Renta eliminada exitosamente.")
        else:
            print("⚠️ No se encontró una renta con ese ID.")
    except mysql.connector.Error as err:
        print(f"❌ No se ha podido eliminar la renta. Error: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

#MOSTRAR RENTAS

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

#EDITAR RENTA

def actualizar_renta(id_renta, id_empleado, fecha_inicio, fecha_devolucion_real,
                     fecha_devolucion_esperada, estado_renta, hora_transaccion, tipo):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = """
        UPDATE Renta
        SET ID_Empleado = %s,
            fecha_inicio = %s,
            fecha_devolucion_real = %s,
            fecha_devolucion_esperada = %s,
            estado_renta = %s,
            hora_transaccion = %s,
            Tipo = %s
        WHERE ID_Renta = %s
        """
        valores = (id_empleado, fecha_inicio, fecha_devolucion_real,
                   fecha_devolucion_esperada, estado_renta, hora_transaccion,
                   tipo, id_renta)
        cursor.execute(sql, valores)
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Renta actualizada exitosamente.")
        else:
            print("⚠️ No se encontró una renta con ese ID.")
    except mysql.connector.Error as err:
        print(f"❌ No se pudo actualizar la renta. Error: {err}")
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

#CRUD METODO DE PAGO

#AGREGAR METODO DE PAGO

def agregar_metodo_pago(id_pago, id_renta, tipo_pago):
    try:
        if tipo_pago not in ['deposito', 'efectivo', 'transaccion']:
            print("❌ Tipo de pago inválido. Debe ser: 'deposito', 'efectivo' o 'transaccion'.")
            return

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Metodo_Pago (ID_Pago, ID_Renta, tipo_pago) VALUES (%s, %s, %s)", 
                       (id_pago, id_renta, tipo_pago))
        conexion.commit()
        print("✅ Método de pago agregado correctamente.")
    except mysql.connector.Error as e:
        print(f"❌ Error al agregar método de pago: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#MOSTRAR METODO DE PAGO

def mostrar_metodos_pago():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT ID_Pago, ID_Renta, tipo_pago FROM Metodo_Pago")
        resultados = cursor.fetchall()
        print(tabulate(resultados, headers=["ID Pago", "ID Renta", "Tipo de Pago"], tablefmt="fancy_grid"))
    except mysql.connector.Error as e:
        print(f"❌ Error al obtener métodos de pago: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#ACTUALIZAR METODO DE PAGO

def actualizar_metodo_pago(id_pago, nuevo_id_renta, nuevo_tipo_pago):
    try:
        if nuevo_tipo_pago not in ['deposito', 'efectivo', 'transaccion']:
            print("❌ Tipo de pago inválido. Debe ser: 'deposito', 'efectivo' o 'transaccion'.")
            return

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE Metodo_Pago SET ID_Renta = %s, tipo_pago = %s WHERE ID_Pago = %s",
                       (nuevo_id_renta, nuevo_tipo_pago, id_pago))
        if cursor.rowcount == 0:
            print("⚠️ No se encontró ningún método de pago con ese ID.")
        else:
            conexion.commit()
            print("✅ Método de pago actualizado correctamente.")
    except mysql.connector.Error as e:
        print(f"❌ Error al actualizar método de pago: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#ELIMINAR METODO DE PAGO

def eliminar_metodo_pago(id_pago):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Metodo_Pago WHERE ID_Pago = %s", (id_pago,))
        if cursor.rowcount == 0:
            print("⚠️ No se encontró ningún método de pago con ese ID.")
        else:
            conexion.commit()
            print("✅ Método de pago eliminado correctamente.")
    except mysql.connector.Error as e:
        print(f"❌ Error al eliminar método de pago: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()



#CRUD MULTAS

#AÑADIR MULTA

def agregar_multa(id_multa, id_cliente, id_renta, fecha_inicio,
                  fecha_fin, motivo, monto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO Multa (ID_Multa, ID_Cliente, ID_Renta, fecha_inicio, fecha_fin, motivo, monto) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (id_multa, id_cliente, id_renta, fecha_inicio, fecha_fin, motivo, monto)
        )
        conexion.commit()
        print("✅ Multa agregada exitosamente.")
    except mysql.connector.Error as error:
        print(f"❌ Error al agregar la multa: {error}")
    finally:
        cursor.close()
        conexion.close()


#ELIMINAR MULTA 
def eliminar_multa(id_multa):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = "DELETE FROM Multa WHERE ID_Multa = %s"
        cursor.execute(sql, (id_multa,))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Multa eliminada exitosamente.")
        else:
            print("⚠️ No se encontró una multa con ese ID.")
    except mysql.connector.Error as err:
        print(f"❌ No se ha podido eliminar la multa. Error: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

#ACTUALIZAR MULTA
def actualizar_multa(id_multa, id_cliente, id_renta, fecha_inicio,
                     fecha_fin, motivo, monto):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = """
        UPDATE Multa
        SET ID_Cliente = %s,
            ID_Renta = %s,
            fecha_inicio = %s,
            fecha_fin = %s,
            motivo = %s,
            monto = %s
        WHERE ID_Multa = %s
        """
        valores = (id_cliente, id_renta, fecha_inicio, fecha_fin, motivo, monto, id_multa)
        cursor.execute(sql, valores)
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Multa actualizada exitosamente.")
        else:
            print("⚠️ No se encontró una multa con ese ID.")
    except mysql.connector.Error as err:
        print(f"❌ No se pudo actualizar la multa. Error: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


#MOSTRAR MULTA
def mostrar_multas():
    print("\n🧾 Multas registradas:\n")

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        query = """
        SELECT 
            Multa.ID_Multa,
            Cliente.nombre_completo AS Nombre_Cliente,
            Multa.ID_Renta,
            Multa.fecha_inicio,
            Multa.fecha_fin,
            Multa.motivo,
            Multa.monto
        FROM Multa
        JOIN Cliente ON Multa.ID_Cliente = Cliente.ID_Cliente
        ORDER BY Multa.ID_Multa;
        """


        cursor.execute(query)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        if resultados:
            print(tabulate(resultados, headers=columnas, tablefmt="fancy_grid"))
        else:
            print("No hay multas registradas.")

    except mysql.connector.Error as err:
        print("❌ Error al conectar o consultar la base de datos:", err)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

    time.sleep(1.5)
