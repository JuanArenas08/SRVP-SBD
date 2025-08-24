import mysql.connector
from conexion import *
from tabulate import tabulate
from datetime import datetime
import time


# CRUD CLIENTE - MODIFICADO PARA USAR STORED PROCEDURES

# AÑADIR CLIENTE
def agregar_cliente(id_cliente, email, historial, nombre_completo, telefono):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Llamar al stored procedure para crear cliente
        cursor.callproc('sp_crear_cliente', (id_cliente, email, historial, nombre_completo, telefono))
        conn.commit()
        
        print("✅ Cliente agregado exitosamente.")
        
    except mysql.connector.Error as err:
        print(f"❌ Error al agregar el cliente: {err}")
        if "El ID de cliente ya existe" in str(err):
            print("⚠️ Ya existe un cliente con ese ID.")
        elif "El formato del email no es válido" in str(err):
            print("⚠️ El formato del email no es válido.")
        elif "El historial debe ser" in str(err):
            print("⚠️ El historial debe ser: Mala, Baja, Regular, Buena o Excelente")
        elif "El nombre completo debe tener" in str(err):
            print("⚠️ El nombre completo debe tener al menos 2 caracteres.")
        elif "El teléfono debe tener" in str(err):
            print("⚠️ El teléfono debe tener exactamente 10 dígitos.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# CONSULTAR CLIENTES
def mostrar_clientes():
    print("\n👥 Lista de Clientes Registrados:")
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Llamar al stored procedure para leer clientes
        cursor.callproc('sp_leer_clientes')
        
        resultados = []
        headers = ["ID_Cliente", "email", "historial", "nombre_completo", "telefono"]
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("ℹ️ No hay clientes registrados.")
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al consultar clientes: {err}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

    time.sleep(1.5)

# EDITAR CLIENTE
def actualizar_cliente(id_cliente, email, historial, nombre_completo, telefono):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Llamar al stored procedure para actualizar cliente
        cursor.callproc('sp_actualizar_cliente', (id_cliente, email, historial, nombre_completo, telefono))
        conn.commit()
        
        if cursor.rowcount > 0:
            print("✅ Cliente actualizado exitosamente.")
        else:
            print("⚠️ No se encontró un cliente con ese ID.")
            
    except mysql.connector.Error as err:
        print(f"❌ Error al actualizar el cliente: {err}")
        if "El ID de cliente no existe" in str(err):
            print("⚠️ No existe un cliente con ese ID.")
        elif "El formato del email no es válido" in str(err):
            print("⚠️ El formato del email no es válido.")
        elif "El historial debe ser" in str(err):
            print("⚠️ El historial debe ser: Mala, Baja, Regular, Buena o Excelente")
        elif "El nombre completo debe tener" in str(err):
            print("⚠️ El nombre completo debe tener al menos 2 caracteres.")
        elif "El teléfono debe tener" in str(err):
            print("⚠️ El teléfono debe tener exactamente 10 dígitos.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# ELIMINAR CLIENTE
def eliminar_cliente(id_cliente):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Llamar al stored procedure para eliminar cliente
        cursor.callproc('sp_eliminar_cliente', (id_cliente,))
        conn.commit()

        print("✅ Cliente eliminado exitosamente.")

    except mysql.connector.Error as err:
        print(f"❌ Error al eliminar el cliente: {err}")
        if "El ID de cliente no existe" in str(err):
            print("⚠️ No existe un cliente con ese ID.")
        elif "No se puede eliminar el cliente porque tiene transacciones asociadas" in str(err):
            print("⚠️ No se puede eliminar el cliente porque tiene transacciones asociadas.")
        elif "No se puede eliminar el cliente porque tiene multas asociadas" in str(err):
            print("⚠️ No se puede eliminar el cliente porque tiene multas asociadas.")
        elif "No se puede eliminar el cliente porque tiene rentas asociadas" in str(err):
            print("⚠️ No se puede eliminar el cliente porque tiene rentas asociadas.")
        elif "No se puede eliminar el cliente porque tiene rentas en pareja asociadas" in str(err):
            print("⚠️ No se puede eliminar el cliente porque tiene rentas en pareja asociadas.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
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

#MODIFICACIÓN CON EL TRIGGER CREADO
# CRUD RENTAS - MODIFICADO PARA USAR STORED PROCEDURES

# AGREGAR RENTA
def agregar_renta(id_renta, id_empleado, fecha_inicio,
                  fecha_devolucion_real, fecha_devolucion_esperada,
                  estado_renta, hora_transaccion, tipo, descuento=0):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Convertir hora de formato HHMM a TIME
        hora_formateada = f"{hora_transaccion[:2]}:{hora_transaccion[2:4]}:00"
        
        # Llamar al stored procedure para crear renta
        cursor.callproc('sp_crear_renta', (
            int(id_renta), int(id_empleado), fecha_inicio,
            fecha_devolucion_real, fecha_devolucion_esperada,
            estado_renta, hora_formateada, tipo, descuento
        ))
        conn.commit()
        
        print("✅ Renta agregada exitosamente.")
        
    except mysql.connector.Error as err:
        print(f"❌ Error al agregar la renta: {err}")
        if "El ID de renta ya existe" in str(err):
            print("⚠️ Ya existe una renta con ese ID.")
        elif "El ID de empleado no existe" in str(err):
            print("⚠️ El ID de empleado no existe.")
        elif "El estado de renta debe ser" in str(err):
            print("⚠️ El estado de renta debe ser: Activo, Finalizado o Atrasada")
        elif "El tipo debe ser" in str(err):
            print("⚠️ El tipo debe ser: PS PLUS o VIDEOJUEGO")
        elif "La fecha de devolución esperada no puede ser anterior" in str(err):
            print("⚠️ La fecha de devolución esperada no puede ser anterior a la fecha de inicio")
        elif "La fecha de devolución real no puede ser anterior" in str(err):
            print("⚠️ La fecha de devolución real no puede ser anterior a la fecha de inicio")
        elif "El año de la fecha de inicio debe estar" in str(err):
            print("⚠️ El año de la fecha de inicio debe estar entre 2000 y 2100")
        elif "La hora debe estar entre" in str(err):
            print("⚠️ La hora debe tener un formato válido (HH:MM:SS)")
        elif "El descuento debe ser" in str(err):
            print("⚠️ El descuento debe ser 0 (falso) o 1 (verdadero)")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# MOSTRAR RENTAS
def mostrar_rentas():
    print("\n🧾 Rentas Actuales:\n")
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Llamar al stored procedure para leer rentas
        cursor.callproc('sp_leer_rentas')
        
        resultados = []
        headers = ["ID_Renta", "ID_Empleado", "nombre_empleado", "fecha_inicio", 
                  "fecha_devolucion_esperada", "fecha_devolucion_real", "estado_renta",
                  "hora_transaccion", "descuento", "Tipo"]
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("No hay rentas registradas.")
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al consultar la base de datos: {err}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

    time.sleep(1.5)

# EDITAR RENTA
def actualizar_renta(id_renta, id_empleado, fecha_inicio, fecha_devolucion_real,
                     fecha_devolucion_esperada, estado_renta, hora_transaccion, tipo):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Convertir hora de formato HHMM a TIME
        hora_formateada = f"{hora_transaccion[:2]}:{hora_transaccion[2:4]}:00"
        
        # Llamar al stored procedure para actualizar renta
        cursor.callproc('sp_actualizar_renta', (
            int(id_renta), int(id_empleado), fecha_inicio,
            fecha_devolucion_real, fecha_devolucion_esperada,
            estado_renta, hora_formateada, tipo, 0  # descuento por defecto 0
        ))
        conn.commit()
        
        if cursor.rowcount > 0:
            print("✅ Renta actualizada exitosamente.")
        else:
            print("⚠️ No se encontró una renta con ese ID.")
            
    except mysql.connector.Error as err:
        print(f"❌ Error al actualizar la renta: {err}")
        if "El ID de renta no existe" in str(err):
            print("⚠️ No existe una renta con ese ID.")
        elif "El ID de empleado no existe" in str(err):
            print("⚠️ El ID de empleado no existe.")
        elif "El estado de renta debe ser" in str(err):
            print("⚠️ El estado de renta debe ser: Activo, Finalizado o Atrasada")
        elif "El tipo debe ser" in str(err):
            print("⚠️ El tipo debe ser: PS PLUS o VIDEOJUEGO")
        elif "La fecha de devolución esperada no puede ser anterior" in str(err):
            print("⚠️ La fecha de devolución esperada no puede ser anterior a la fecha de inicio")
        elif "La fecha de devolución real no puede ser anterior" in str(err):
            print("⚠️ La fecha de devolución real no puede ser anterior to the fecha de inicio")
        elif "El año de la fecha de inicio debe estar" in str(err):
            print("⚠️ El año de la fecha de inicio debe estar entre 2000 y 2100")
        elif "La hora debe estar entre" in str(err):
            print("⚠️ La hora debe tener un formato válido (HH:MM:SS)")
        elif "El descuento debe ser" in str(err):
            print("⚠️ El descuento debe ser 0 (falso) o 1 (verdadero)")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# ELIMINAR RENTA
def eliminar_renta(id_renta):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Llamar al stored procedure para eliminar renta
        cursor.callproc('sp_eliminar_renta', (int(id_renta),))
        conn.commit()

        print("✅ Renta eliminada exitosamente.")

    except mysql.connector.Error as err:
        print(f"❌ Error al eliminar la renta: {err}")
        if "El ID de renta no existe" in str(err):
            print("⚠️ No existe una renta con ese ID.")
        elif "No se puede eliminar la renta porque tiene transacciones asociadas" in str(err):
            print("⚠️ No se puede eliminar la renta porque tiene transacciones asociadas.")
        elif "No se puede eliminar la renta porque tiene multas asociadas" in str(err):
            print("⚠️ No se puede eliminar la renta porque tiene multas asociadas.")
        elif "No se puede eliminar la renta porque tiene métodos de pago asociados" in str(err):
            print("⚠️ No se puede eliminar la renta porque tiene métodos de pago asociados.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
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

        # Llamar al stored procedure para crear empleado
        cursor.callproc('sp_crear_empleado', (int(id_empleado), rol, nombre))
        conexion.commit()

        print("✅ Empleado agregado exitosamente.")

        # Mostrar todos los empleados después de agregar
        cursor.callproc('sp_leer_empleados')
        resultados = []
        for result in cursor.stored_results():
            resultados = result.fetchall()
        
        if resultados:
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("ℹ️ No hay empleados registrados.")

    except mysql.connector.Error as err:
        print(f"❌ Error al agregar el empleado: {err}")
        if "El ID de empleado ya existe" in str(err):
            print("⚠️ Ya existe un empleado con ese ID.")
        elif "El rol debe ser" in str(err):
            print("⚠️ El rol debe ser: Administrador, Vendedor o Soporte.")

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()


# Mostrar empleados

def mostrar_empleados():
    print("\n📋 Lista de empleados:")
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Llamar al stored procedure para leer empleados
        cursor.callproc('sp_leer_empleados')
        
        resultados = []
        headers = []  # Inicializar headers como lista vacía
        for result in cursor.stored_results():
            resultados = result.fetchall()
            # Obtener los nombres de las columnas
            if cursor.description:
                headers = [desc[0] for desc in cursor.description]
        
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("ℹ️ No hay empleados registrados.")
            # Definir headers básicos si no hay resultados pero queremos mostrar estructura
            if not headers:
                headers = ["ID_Empleado","rol","nombre"]
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al consultar empleados: {err}")

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

# Editar empleado

def editar_empleado():
    print("\n✏️ Editar empleado:")
    
    try:
        # Primero mostrar todos los empleados para que el usuario elija
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc('sp_leer_empleados')
        
        resultados = []
        headers = ["ID_Empleado", "rol", "nombre"]  # Headers por defecto
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if not resultados:
            print("❌ No hay empleados registrados.")
            return
            
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        
        id_empleado = input("\nIngrese el ID del empleado a editar: ").strip()
        
        if not id_empleado.isdigit():
            print("❌ El ID debe ser un número.")
            return
            
        # Verificar que el empleado existe usando el stored procedure
        cursor.callproc('sp_leer_empleados')
        empleado_encontrado = None
        for result in cursor.stored_results():
            empleados = result.fetchall()
            for empleado in empleados:
                if empleado[0] == int(id_empleado):
                    empleado_encontrado = empleado
                    break
        
        if not empleado_encontrado:
            print("❌ Empleado no encontrado.")
            return
            
        print(f"\nEditando empleado: {empleado_encontrado[2]} (ID: {empleado_encontrado[0]}, Rol: {empleado_encontrado[1]})")
        
        nuevo_nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ").strip()
        nuevo_rol = input("Nuevo rol (dejar en blanco para no cambiar): ").strip()

        # Si no se ingresaron nuevos valores, mantener los actuales
        if not nuevo_nombre:
            nuevo_nombre = empleado_encontrado[2]
        if not nuevo_rol:
            nuevo_rol = empleado_encontrado[1]

        # Llamar al stored procedure para actualizar empleado
        cursor.callproc('sp_actualizar_empleado', (int(id_empleado), nuevo_rol, nuevo_nombre))
        conexion.commit()

        print("✅ Empleado actualizado.")
        
        # Mostrar empleados actualizados
        cursor.callproc('sp_leer_empleados')
        resultados = []
        headers = ["ID_Empleado", "rol", "nombre"]  # Headers por defecto
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("ℹ️ No hay empleados registrados.")
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al editar empleado: {err}")
        if "El ID de empleado no existe" in str(err):
            print("⚠️ No existe un empleado con ese ID.")
        elif "El rol debe ser" in str(err):
            print("⚠️ El rol debe ser: Administrador, Vendedor o Soporte.")

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

# Eliminar empleado

def eliminar_empleado():
    print("\n🗑️ Eliminar empleado:")
    
    try:
        # Primero mostrar todos los empleados para que el usuario elija
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc('sp_leer_empleados')
        
        resultados = []
        headers = ["ID_Empleado", "rol", "nombre"]  # Headers por defecto
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if not resultados:
            print("❌ No hay empleados registrados.")
            return
            
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        
        id_empleado = input("\nIngrese el ID del empleado a eliminar: ").strip()
        
        if not id_empleado.isdigit():
            print("❌ El ID debe ser un número.")
            return
            
        # Verificar que el empleado existe usando el stored procedure
        cursor.callproc('sp_leer_empleados')
        empleado_encontrado = None
        for result in cursor.stored_results():
            empleados = result.fetchall()
            for empleado in empleados:
                if empleado[0] == int(id_empleado):
                    empleado_encontrado = empleado
                    break
        
        if not empleado_encontrado:
            print("❌ Empleado no encontrado.")
            return
            
        print(f"\nEmpleado a eliminar: {empleado_encontrado[2]} (ID: {empleado_encontrado[0]}, Rol: {empleado_encontrado[1]})")
        
        confirmar = input("¿Está seguro que desea eliminar este empleado? (s/n): ").strip().lower()
        if confirmar != "s":
            print("❌ Operación cancelada.")
            return

        # Llamar al stored procedure para eliminar empleado
        cursor.callproc('sp_eliminar_empleado', (int(id_empleado),))
        conexion.commit()

        print("✅ Empleado eliminado.")
        
        # Mostrar empleados actualizados
        cursor.callproc('sp_leer_empleados')
        resultados = []
        headers = ["ID_Empleado", "rol", "nombre"]  # Headers por defecto
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("ℹ️ No hay empleados registrados.")
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al eliminar empleado: {err}")
        if "El ID de empleado no existe" in str(err):
            print("⚠️ No existe un empleado con ese ID.")
        elif "No se puede eliminar el empleado porque tiene rentas asociadas" in str(err):
            print("⚠️ No se puede eliminar el empleado porque tiene rentas asociadas.")
        elif "No se puede eliminar el empleado porque tiene multas asociadas" in str(err):
            print("⚠️ No se puede eliminar el empleado porque tiene multas asociadas.")

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

#CRUD METODO DE PAGO

#AGREGAR METODO DE PAGO

def agregar_metodo_pago(id_pago, tipo_pago):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Llamar al stored procedure para crear método de pago
        cursor.callproc('sp_crear_metodo_pago', (id_pago, tipo_pago))
        conexion.commit()
        
        print("✅ Método de pago agregado correctamente.")
        
    except mysql.connector.Error as e:
        print(f"❌ Error al agregar método de pago: {e}")
        if "El ID de método de pago ya existe" in str(e):
            print("⚠️ Ya existe un método de pago con ese ID.")
        elif "El tipo de pago debe ser" in str(e):
            print("⚠️ El tipo de pago debe ser: deposito, efectivo o transaccion")
            
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#MOSTRAR METODO DE PAGO

def mostrar_metodos_pago():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Llamar al stored procedure para leer métodos de pago
        cursor.callproc('sp_leer_metodos_pago')
        
        resultados = []
        headers = ["ID_Pago", "tipo_pago", "ID_Transaccion", "ID_Cliente", 
                  "nombre_cliente", "fecha", "hora", "monto_total"]
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if resultados:
            print("\n💳 Métodos de Pago Registrados:")
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("ℹ️ No hay métodos de pago registrados.")
            
    except mysql.connector.Error as e:
        print(f"❌ Error al obtener métodos de pago: {e}")
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#ACTUALIZAR METODO DE PAGO

def actualizar_metodo_pago(id_pago, nuevo_tipo_pago):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Llamar al stored procedure para actualizar método de pago
        cursor.callproc('sp_actualizar_metodo_pago', (id_pago, nuevo_tipo_pago))
        conexion.commit()
        
        print("✅ Método de pago actualizado correctamente.")
            
    except mysql.connector.Error as e:
        print(f"❌ Error al actualizar método de pago: {e}")
        if "El ID de método de pago no existe" in str(e):
            print("⚠️ No existe un método de pago con ese ID.")
        elif "El tipo de pago debe ser" in str(e):
            print("⚠️ El tipo de pago debe ser: deposito, efectivo o transaccion")
            
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#ELIMINAR METODO DE PAGO

def eliminar_metodo_pago(id_pago):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Llamar al stored procedure para eliminar método de pago
        cursor.callproc('sp_eliminar_metodo_pago', (id_pago,))
        conexion.commit()
        
        print("✅ Método de pago eliminado correctamente.")
            
    except mysql.connector.Error as e:
        print(f"❌ Error al eliminar método de pago: {e}")
        if "El ID de método de pago no existe" in str(e):
            print("⚠️ No existe un método de pago con ese ID.")
            
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()



#CRUD MULTAS

# CRUD MULTAS - MODIFICADO PARA USAR STORED PROCEDURES

# AÑADIR MULTA
def agregar_multa(id_multa, id_cliente, id_renta, fecha_inicio, fecha_fin, motivo, monto):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Llamar al stored procedure para crear multa
        cursor.callproc('sp_crear_multa', (
            int(id_multa), int(id_cliente), int(id_renta), 
            fecha_inicio, fecha_fin, motivo, int(monto)
        ))
        conn.commit()
        
        print("✅ Multa agregada exitosamente.")
        
    except mysql.connector.Error as err:
        print(f"❌ Error al agregar la multa: {err}")
        if "El ID de multa ya existe" in str(err):
            print("⚠️ Ya existe una multa con ese ID.")
        elif "El ID de cliente no existe" in str(err):
            print("⚠️ El ID de cliente no existe.")
        elif "El ID de renta no existe" in str(err):
            print("⚠️ El ID de renta no existe.")
        elif "La fecha de fin no puede ser anterior" in str(err):
            print("⚠️ La fecha de fin no puede ser anterior a la fecha de inicio.")
        elif "El año de la fecha de inicio debe estar" in str(err):
            print("⚠️ El año de la fecha de inicio debe estar entre 2000 y 2100.")
        elif "El año de la fecha de fin debe estar" in str(err):
            print("⚠️ El año de la fecha de fin debe estar entre 2000 y 2100.")
        elif "El monto debe ser mayor a 0" in str(err):
            print("⚠️ El monto debe ser mayor a 0.")
        elif "El motivo no puede estar vacío" in str(err):
            print("⚠️ El motivo no puede estar vacío.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# MOSTRAR MULTAS
def mostrar_multas():
    print("\n🧾 Multas registradas:\n")
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Llamar al stored procedure para leer multas
        cursor.callproc('sp_leer_multas')
        
        resultados = []
        headers = ["ID_Multa", "ID_Cliente", "nombre_cliente", "ID_Renta", 
                  "tipo_renta", "fecha_inicio", "fecha_fin", "motivo", "monto"]
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("No hay multas registradas.")
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al consultar la base de datos: {err}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

    time.sleep(1.5)

# ACTUALIZAR MULTA
def actualizar_multa(id_multa, id_cliente, id_renta, fecha_inicio, fecha_fin, motivo, monto):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Llamar al stored procedure para actualizar multa
        cursor.callproc('sp_actualizar_multa', (
            int(id_multa), int(id_cliente), int(id_renta), 
            fecha_inicio, fecha_fin, motivo, int(monto)
        ))
        conn.commit()
        
        if cursor.rowcount > 0:
            print("✅ Multa actualizada exitosamente.")
        else:
            print("⚠️ No se encontró una multa con ese ID.")
            
    except mysql.connector.Error as err:
        print(f"❌ Error al actualizar la multa: {err}")
        if "El ID de multa no existe" in str(err):
            print("⚠️ No existe una multa con ese ID.")
        elif "El ID de cliente no existe" in str(err):
            print("⚠️ El ID de cliente no existe.")
        elif "El ID de renta no existe" in str(err):
            print("⚠️ El ID de renta no existe.")
        elif "La fecha de fin no puede ser anterior" in str(err):
            print("⚠️ La fecha de fin no puede ser anterior a la fecha de inicio.")
        elif "El año de la fecha de inicio debe estar" in str(err):
            print("⚠️ El año de la fecha de inicio debe estar entre 2000 y 2100.")
        elif "El año de la fecha de fin debe estar" in str(err):
            print("⚠️ El año de la fecha de fin debe estar entre 2000 y 2100.")
        elif "El monto debe ser mayor a 0" in str(err):
            print("⚠️ El monto debe ser mayor a 0.")
        elif "El motivo no puede estar vacío" in str(err):
            print("⚠️ El motivo no puede estar vacío.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# ELIMINAR MULTA
def eliminar_multa(id_multa):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Llamar al stored procedure para eliminar multa
        cursor.callproc('sp_eliminar_multa', (int(id_multa),))
        conn.commit()

        print("✅ Multa eliminada exitosamente.")

    except mysql.connector.Error as err:
        print(f"❌ Error al eliminar la multa: {err}")
        if "El ID de multa no existe" in str(err):
            print("⚠️ No existe una multa con ese ID.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


# CRUD TRANSACCIONES
#AÑADIR TRANSACCION

def agregar_transaccion(id_transaccion, id_cliente, fecha, hora, monto_total):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Llamar al stored procedure para crear transacción
        cursor.callproc('sp_crear_transaccion', (id_transaccion, id_cliente, fecha, hora, monto_total))
        conn.commit()
        
        print("✅ Transacción agregada exitosamente.")
        
    except mysql.connector.Error as err:
        print(f"❌ Error al agregar la transacción: {err}")
        if "El ID de transacción ya existe" in str(err):
            print("⚠️ Ya existe una transacción con ese ID.")
        elif "El ID de cliente no existe" in str(err):
            print("⚠️ El ID de cliente no existe.")
        elif "La hora debe estar entre" in str(err):
            print("⚠️ La hora debe tener un formato válido (HH:MM:SS).")
        elif "El año de la fecha debe estar entre" in str(err):
            print("⚠️ La fecha debe estar entre los años 2000 y 2100.")
        elif "El monto total debe ser mayor a 0" in str(err):
            print("⚠️ El monto total debe ser mayor a 0.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


#ELIMINAR TRANSACCION
def eliminar_transaccion(id_transaccion):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Llamar al stored procedure para eliminar transacción
        cursor.callproc('sp_eliminar_transaccion', (id_transaccion,))
        conn.commit()

        print("✅ Transacción eliminada exitosamente.")

    except mysql.connector.Error as err:
        print(f"❌ Error al eliminar la transacción: {err}")
        if "El ID de transacción no existe" in str(err):
            print("⚠️ No existe una transacción con ese ID.")
        elif "No se puede eliminar la transacción porque tiene rentas asociadas" in str(err):
            print("⚠️ No se puede eliminar la transacción porque tiene rentas asociadas.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

#ACTUALIZAR TRANSACCION
def actualizar_transaccion(id_transaccion, id_cliente, fecha, hora, monto_total):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Llamar al stored procedure para actualizar transacción
        cursor.callproc('sp_actualizar_transaccion', (id_transaccion, id_cliente, fecha, hora, monto_total))
        conn.commit()
        
        if cursor.rowcount > 0:
            print("✅ Transacción actualizada exitosamente.")
        else:
            print("⚠️ No se encontró una transacción con ese ID.")
            
    except mysql.connector.Error as err:
        print(f"❌ Error al actualizar la transacción: {err}")
        if "El ID de transacción no existe" in str(err):
            print("⚠️ No existe una transacción con ese ID.")
        elif "El ID de cliente no existe" in str(err):
            print("⚠️ El ID de cliente no existe.")
        elif "La hora debe estar entre" in str(err):
            print("⚠️ La hora debe tener un formato válido (HH:MM:SS).")
        elif "El año de la fecha debe estar entre" in str(err):
            print("⚠️ La fecha debe estar entre los años 2000 y 2100.")
        elif "El monto total debe ser mayor a 0" in str(err):
            print("⚠️ El monto total debe ser mayor a 0.")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

#MOSTRAR TRANSACCION
def mostrar_transacciones():
    print("\n💰 Transacciones registradas:\n")
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Llamar al stored procedure para leer transacciones
        cursor.callproc('sp_leer_transacciones')
        
        resultados = []
        headers = ["ID", "ID_Cliente", "nombre_cliente", "fecha", "hora", 
                  "monto_total", "ID_Renta", "estado_renta", "tipo_renta"]
        
        for result in cursor.stored_results():
            resultados = result.fetchall()
            if result.description:
                headers = [desc[0] for desc in result.description]
        
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print("No hay transacciones registradas.")
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al consultar la base de datos: {err}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

    time.sleep(1.5)


# FUNCIONES PARA LAS VIEWS - Agregar al final de crud.py

def mostrar_clientes_frecuentes():
    print("\n🏆 Clientes Más Frecuentes:")
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # DEBUG: Verificar la base de datos actual
        cursor.execute("SELECT DATABASE()")
        db_actual = cursor.fetchone()[0]
        print(f"📋 Conectado a la base de datos: {db_actual}")
        
        # DEBUG: Verificar si la view existe
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.VIEWS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'clientes_frecuentes'
        """)
        view_existe = cursor.fetchone()
        
        if view_existe:
            print("✅ View 'clientes_frecuentes' encontrada")
            # Consultar la view
            cursor.execute("SELECT * FROM clientes_frecuentes")
        else:
            print("⚠️ View no encontrada, usando consulta directa")
            # Consulta directa alternativa
            cursor.execute("""
                SELECT 
                    c.ID_Cliente, 
                    c.nombre_completo, 
                    c.telefono, 
                    c.email, 
                    COUNT(r.ID_Renta) AS total_rentas
                FROM cliente c
                JOIN realiza rl ON c.ID_Cliente = rl.ID_Cliente
                JOIN renta r ON rl.ID_Renta = r.ID_Renta
                GROUP BY c.ID_Cliente, c.nombre_completo, c.telefono, c.email
                ORDER BY total_rentas DESC
            """)
        
        resultados = cursor.fetchall()
        headers = [i[0] for i in cursor.description] 
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
            print(f"📊 Total de clientes: {len(resultados)}")
        else:
            print("ℹ️ No hay datos de clientes frecuentes.")
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al consultar clientes frecuentes: {err}")
        print("💡 Ejecuta en MySQL: SHOW FULL TABLES WHERE TABLE_TYPE LIKE 'VIEW'")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

    time.sleep(2)

def mostrar_videojuegos_mas_rentados():
    print("\n🎮 Videojuegos Más Rentados:")
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # DEBUG: Verificar la base de datos actual
        cursor.execute("SELECT DATABASE()")
        db_actual = cursor.fetchone()[0]
        print(f"📋 Conectado a la base de datos: {db_actual}")
        
        # DEBUG: Verificar si la view existe
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.VIEWS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'videojuegos_mas_rentados'
        """)
        view_existe = cursor.fetchone()
        
        if view_existe:
            print("✅ View 'videojuegos_mas_rentados' encontrada")
            # Consultar la view
            cursor.execute("SELECT * FROM videojuegos_mas_rentados")
        else:
            print("⚠️ View no encontrada, usando consulta directa")
            # Consulta directa alternativa
            cursor.execute("""
                SELECT 
                    v.ID AS ID_Videojuego, 
                    v.titulo, 
                    v.plataforma, 
                    COUNT(r.ID_Renta) AS veces_rentado
                FROM videojuego v
                JOIN renta r ON v.ID = r.ID_Renta
                GROUP BY v.ID, v.titulo, v.plataforma
                ORDER BY veces_rentado DESC
            """)
        
        resultados = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        
        if resultados:
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
            print(f"🎯 Total de videojuegos: {len(resultados)}")
        else:
            print("ℹ️ No hay datos de videojuegos rentados.")
            print(tabulate([], headers=headers, tablefmt="fancy_grid"))

    except mysql.connector.Error as err:
        print(f"❌ Error al consultar videojuegos más rentados: {err}")
        print("💡 Ejecuta en MySQL: SHOW FULL TABLES WHERE TABLE_TYPE LIKE 'VIEW'")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

    time.sleep(2)

# FUNCIÓN ADICIONAL PARA MOSTRAR DETALLES DE RENTAS POR CLIENTE
def mostrar_detalles_rentas_cliente(id_cliente):
    """Muestra el detalle completo de las rentas de un cliente específico"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = """
        SELECT 
            r.ID_Renta,
            r.fecha_inicio,
            r.fecha_devolucion_esperada,
            r.fecha_devolucion_real,
            r.estado_renta,
            r.Tipo,
            v.titulo AS videojuego,
            v.plataforma,
            e.nombre AS empleado
        FROM renta r
        JOIN realiza rl ON r.ID_Renta = rl.ID_Renta
        LEFT JOIN videojuego v ON r.ID_Renta = v.ID
        JOIN empleado e ON r.ID_Empleado = e.ID_Empleado
        WHERE rl.ID_Cliente = %s
        ORDER BY r.fecha_inicio DESC
        """
        
        cursor.execute(query, (id_cliente,))
        resultados = cursor.fetchall()
        
        if resultados:
            headers = [desc[0] for desc in cursor.description]
            print(f"\n📋 Detalles de rentas para el cliente ID: {id_cliente}")
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        else:
            print(f"ℹ️ El cliente ID {id_cliente} no tiene rentas registradas.")
            
    except mysql.connector.Error as err:
        print(f"❌ Error al consultar detalles: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()