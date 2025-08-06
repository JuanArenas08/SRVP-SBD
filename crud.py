import mysql.connector

#CONECTAMOS A LA BASE DE DATOS

def conectar():
    return mysql.connector.connect(
        user="root",
        password="admin",
        host="hostname",
        database="srvp",
        port=3306
    )

#CRUD CLIENTE
#AÑADIR

def agregar_cliente(id_cliente, email, historial, nombre_completo, telefono):
    try:
        conn = conectar()
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

def mostrar_clientes():
    try:
        conn = conectar()
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

#EDITAR

def actualizar_cliente(id_cliente, email, historial, nombre_completo, telefono):
    try:
        conn = conectar()
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
        conn = conectar()
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