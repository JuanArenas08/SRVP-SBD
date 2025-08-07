
import mysql.connector
from conexion import *
from crud import *

def mostrar_menu():
    print("\n¿Qué deseas hacer?")
    print("1️⃣  Mostrar todos los clientes")
    print("2️⃣  Mostrar todas las rentas")
    print("3️⃣  Mostrar los videojuegos disponibles")
    print("0️⃣  Salir")
    print("-" * 50)

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



def rentas():
    while True:
        print("\n¿Qué deseas hacer en Rentas?")
        print("1️⃣  Añadir Renta")
        print("2️⃣  Mostrar todas las Rentas")
        print("3️⃣  Editar Renta")
        print("4️⃣  Eliminar Renta")
        print(" 5  Mostrar Renta de un cliente")
        print("0️⃣  Salir")
        print("-" * 50)

        opc = input("Seleccione una opción: ")

        if opc == "1":
            print("\nIngrese los datos para agregar una nueva Renta:")

            # ✅ Validar ID_Renta único
            while True:
                id_renta = input("ID Renta: ").strip()
                if not id_renta.isdigit():
                    print("⚠️ El ID debe ser un número.")
                    continue
                if id_existe("Renta", "ID_Renta", id_renta):
                    print("⚠️ Ese ID ya existe.")
                    continue
                break

            # ✅ Validar ID_Empleado
            while True:
                id_empleado = input("ID Empleado: ").strip()
                if not id_empleado.isdigit() or not id_existe("Empleado", "ID_Empleado", id_empleado):
                    print("⚠️ Empleado no válido.")
                else:
                    break

            # ✅ Validar fechas
            def validar_fecha(mensaje, fecha_minima=None):
                while True:
                    fecha = input(mensaje).strip()
                    try:
                        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")

                        if fecha_minima and fecha_dt < fecha_minima:
                            print(f"⚠️ La fecha no puede ser anterior a {fecha_minima.strftime('%Y-%m-%d')}.")
                            continue

                        return fecha
                    except ValueError:
                        print("⚠️ Formato inválido (use YYYY-MM-DD).")

            # Primero se valida la fecha de inicio
            fecha_inicio_str = validar_fecha("Fecha de inicio (YYYY-MM-DD): ")
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")

            # Luego se validan las otras dos, usando la fecha de inicio como mínimo
            fecha_devolucion_esperada = validar_fecha("Fecha devolución esperada (YYYY-MM-DD): ", fecha_inicio)
            fecha_devolucion_real = validar_fecha("Fecha devolución real (YYYY-MM-DD): ", fecha_inicio)

            # ✅ Validar estado
            estados = ["Activo", "Finalizado", "Atrasada"]
            while True:
                estado_renta = input("Estado (Activo/Finalizado/Atrasada): ").strip().capitalize()
                if estado_renta not in estados:
                    print("⚠️ Estado inválido.")
                else:
                    break

            # ✅ Validar hora
            while True:
                hora_transaccion = input("Hora transacción (HHMM): ").strip()
                if not hora_transaccion.isdigit() or len(hora_transaccion) != 4:
                    print("⚠️ Hora inválida.")
                else:
                    break

            # ✅ Validar tipo
            tipos = ["PS PLUS", "VIDEOJUEGO"]
            while True:
                tipo = input("Tipo (PS PLUS / VIDEOJUEGO): ").strip().upper()
                if tipo not in tipos:
                    print("⚠️ Tipo inválido.")
                else:
                    break

            agregar_renta(id_renta, id_empleado, fecha_inicio,
                          fecha_devolucion_real, fecha_devolucion_esperada,
                          estado_renta, hora_transaccion, tipo)

        elif opc == "2":
            mostrar_rentas()

        elif opc == "3":
            print("\n✏️ Editar Renta Existente")

            id_renta = input("Ingrese el ID de la renta a editar: ").strip()
            if not id_renta.isdigit() or not id_existe("Renta", "ID_Renta", id_renta):
                print("❌ No existe una renta con ese ID.")
                return

            # Validar nuevo ID de Empleado
            while True:
                id_empleado = input("Nuevo ID Empleado: ").strip()
                if not id_empleado.isdigit() or not id_existe("Empleado", "ID_Empleado", id_empleado):
                    print("⚠️ Empleado no válido.")
                else:
                    break

            # Validar fechas
            def validar_fecha(mensaje):
                while True:
                    fecha = input(mensaje).strip()
                    try:
                        return datetime.strptime(fecha, "%Y-%m-%d").date()
                    except ValueError:
                        print("⚠️ Formato inválido. Usa YYYY-MM-DD.")

            while True:
                fecha_inicio = validar_fecha("Nueva Fecha de inicio (YYYY-MM-DD): ")
                fecha_devolucion_esperada = validar_fecha("Nueva Fecha devolución esperada (YYYY-MM-DD): ")
                fecha_devolucion_real = validar_fecha("Nueva Fecha devolución real (YYYY-MM-DD): ")

                if fecha_devolucion_esperada < fecha_inicio or fecha_devolucion_real < fecha_inicio:
                    print("⚠️ Las fechas de devolución no pueden ser anteriores a la fecha de inicio.")
                else:
                    break

            # Validar estado
            estados = ["Activo", "Finalizado", "Atrasada"]
            while True:
                estado_renta = input("Nuevo Estado (Activo/Finalizado/Atrasada): ").strip().capitalize()
                if estado_renta not in estados:
                    print("⚠️ Estado inválido.")
                else:
                    break

            # Validar hora
            while True:
                hora_transaccion = input("Nueva Hora transacción (HHMM): ").strip()
                if not hora_transaccion.isdigit() or len(hora_transaccion) != 4:
                    print("⚠️ Hora inválida.")
                else:
                    break

            # Validar tipo
            tipos = ["PS PLUS", "VIDEOJUEGO"]
            while True:
                tipo = input("Nuevo Tipo (PS PLUS / VIDEOJUEGO): ").strip().upper()
                if tipo not in tipos:
                    print("⚠️ Tipo inválido.")
                else:
                    break

            actualizar_renta(id_renta, id_empleado, fecha_inicio.strftime("%Y-%m-%d"),
                            fecha_devolucion_real.strftime("%Y-%m-%d"),
                            fecha_devolucion_esperada.strftime("%Y-%m-%d"),
                            estado_renta, hora_transaccion, tipo)


        elif opc == "4":
            print("\nEliminar Renta")
            id_renta = input("Ingrese el ID de la renta a eliminar: ").strip()
            confirmacion = input(f"¿Está seguro que desea eliminar la renta con ID {id_renta}? (s/n): ").strip().lower()
            if confirmacion == "s":
                eliminar_multa(id_renta)
            else:
                print("❌ Operación cancelada por el usuario.")
        elif opc == "5":
            mostrar_rentas_por_cliente()

        elif opc == "0":
            print("Saliendo del menú de Rentas...")
            break

        else:
            print("Opción no válida. Intente nuevamente...")


def clientes():
    while True:
        print("\n¿Qué deseas hacer en Clientes?")
        print("1️⃣  Añadir Cliente")
        print("2️⃣  Mostrar todos los Clientes")
        print("3️⃣  Editar Clientes Existentes")
        print("4️⃣  Eliminar Clientes Existentes")
        print("0️⃣  Salir")
        print("-" * 50)

        opc = input("Seleccione una opción: ")

        if opc == "1":
            print("\nIngrese los datos para agregar un nuevo cliente:")

            # Validar ID único
            while True:
                id_cliente = input("ID Cliente: ").strip()
                if not id_cliente.isdigit():
                    print("⚠️ El ID debe ser un número.")
                    continue

                # Verificar si el ID ya existe en la base
                if id_cliente_existe(id_cliente):
                    print("⚠️ Este ID ya existe. Ingrese otro.")
                    continue
                break

            # Validar email
            while True:
                email = input("Email: ").strip()
                if "@" not in email or "." not in email:
                    print("⚠️ El email no es válido.")
                else:
                    break

            # Validar historial (solo opciones permitidas)
            historial_permitido = ["mala", "baja", "regular", "buena", "excelente"]
            while True:
                historial = input("Historial (mala/baja/regular/buena/excelente): ").strip().lower()
                if historial not in historial_permitido:
                    print("⚠️ Historial inválido. Opciones: mala, baja, regular, buena, excelente.")
                else:
                    historial = historial.capitalize()
                    break

            # Validar nombre completo
            while True:
                nombre_completo = input("Nombre completo: ").strip().title()
                if nombre_completo == "":
                    print("⚠️ El nombre no puede estar vacío.")
                else:
                    break

            # Validar teléfono
            while True:
                telefono = input("Teléfono (10 dígitos): ").strip()
                if not telefono.isdigit() or len(telefono) != 10:
                    print("⚠️ El teléfono debe tener exactamente 10 dígitos.")
                else:
                    break

            agregar_cliente(id_cliente, email, historial, nombre_completo, telefono)

        elif opc == "2":
            mostrar_clientes()

        elif opc == "3":
            print("\nActualizar Cliente")
            id_cliente = input("Ingrese el ID del cliente a actualizar: ").strip()
            email = input("Nuevo Email: ").strip()
            historial = input("Nuevo Historial: ").strip().capitalize()
            nombre_completo = input("Nuevo Nombre Completo: ").strip().title()
            telefono = input("Nuevo Teléfono: ").strip()
            actualizar_cliente(id_cliente, email, historial, nombre_completo, telefono)

        elif opc == "4":
            print("\n🗑️ Eliminar Cliente")
            id_cliente = input("Ingrese el ID del cliente a eliminar: ").strip()

            if not id_cliente.isdigit():
                print("⚠️ El ID debe ser numérico.")
                continue
            if not id_existe("Cliente", "ID_Cliente", id_cliente):
                print("⚠️ No existe un cliente con ese ID.")
                continue

            try:
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("SELECT nombre_completo FROM Cliente WHERE ID_Cliente = %s", (id_cliente,))
                resultado = cursor.fetchone()
                if resultado:
                    nombre_cliente = resultado[0]
                else:
                    print("❌ No se pudo obtener el nombre del cliente.")
                    continue
            except Exception as e:
                print(f"❌ Error al consultar el cliente: {e}")
                continue
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            confirmacion = input(f"¿Está seguro que desea eliminar al cliente: {nombre_cliente}? (s/n): ").strip().lower()
            if confirmacion == "s":
                eliminar_cliente(id_cliente)
            else:
                print("❌ Operación cancelada por el usuario.")


        elif opc == "0":
            print("Saliendo del menú de Clientes...")
            break

        else:
            print("Opción no válida. Intente nuevamente...")


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

# Submenú de la opción para administrar empleados 

def menu_administrar_empleados():
    while True:
        print("\n🛠️ Submenú - Administración de Empleados")
        print("1. Agregar empleado")
        print("2. Mostrar empleados")
        print("3. Editar empleado")
        print("4. Borrar empleado")
        print("0. Volver al menú principal")

        subop = input("Selecciona una opción: ").strip()

        if subop == "1":
            crear_empleado()
        elif subop == "2":
            mostrar_empleados()
        elif subop == "3":
            editar_empleado()
        elif subop == "4":
            eliminar_empleado()
        elif subop == "0":
            break
        else:
            print("❌ Opción inválida.")

        input("\nPresiona Enter para continuar...")

def multas():
    while True:
        print("\n¿Qué deseas hacer en Multas?")
        print("1️⃣  Añadir Multa")
        print("2️⃣  Mostrar todas las Multas")
        print("3️⃣  Editar Multa")
        print("4️⃣  Eliminar Multa")
        print("0️⃣  Salir")
        print("-" * 50)

        opc = input("Seleccione una opción: ")

        if opc == "1":
            print("\nIngrese los datos para agregar una nueva Multa:")

            # Validar ID_Multa único
            while True:
                id_multa = input("ID Multa: ").strip()
                if not id_multa.isdigit():
                    print("⚠️ El ID debe ser un número.")
                    continue
                if id_existe("Multa", "ID_Multa", id_multa):
                    print("⚠️ Ese ID ya existe.")
                    continue
                break

            # Validar ID_Cliente y mostrar confirmación inmediatamente
            while True:
                id_cliente = input("ID Cliente: ").strip()
                if not id_cliente.isdigit() or not id_existe("Cliente", "ID_Cliente", id_cliente):
                    print("⚠️ Cliente no válido.")
                    continue

                try:
                    conn = obtener_conexion()
                    cursor = conn.cursor()
                    cursor.execute("SELECT nombre_completo FROM Cliente WHERE ID_Cliente = %s", (id_cliente,))
                    cliente = cursor.fetchone()

                    if cliente:
                        print(f"➡️ Cliente encontrado: {cliente[0]}")
                        confirmar_cliente = input("¿Desea continuar con este cliente? (s/n): ").strip().lower()
                        if confirmar_cliente == 's':
                            break
                        else:
                            print("❌ Cliente cancelado. Ingrese otro ID.")
                    else:
                        print("❌ Cliente no encontrado.")

                except mysql.connector.Error as err:
                    print(f"❌ Error al consultar cliente: {err}")
                finally:
                    if 'cursor' in locals(): cursor.close()
                    if 'conn' in locals(): conn.close()

            # Validar ID_Renta y mostrar verificación de la renta
            while True:
                id_renta = input("ID Renta asociada: ").strip()
                if not id_renta.isdigit() or not id_existe("Renta", "ID_Renta", id_renta):
                    print("⚠️ Renta no válida.")
                    continue

                try:
                    conn = obtener_conexion()
                    cursor = conn.cursor()
                    cursor.execute("SELECT Tipo FROM Renta WHERE ID_Renta = %s", (id_renta,))
                    renta = cursor.fetchone()

                    if renta:
                        print(f"➡️ Tipo de Renta: {renta[0]}")
                        confirmar_renta = input("¿Desea continuar con esta renta? (s/n): ").strip().lower()
                        if confirmar_renta == 's':
                            break
                        else:
                            print("❌ Renta cancelada. Ingrese otro ID.")
                    else:
                        print("❌ Renta no encontrada.")

                except mysql.connector.Error as err:
                    print(f"❌ Error al consultar renta: {err}")
                finally:
                    if 'cursor' in locals(): cursor.close()
                    if 'conn' in locals(): conn.close()

            # Validar fechas
            def validar_fecha(mensaje):
                while True:
                    fecha = input(mensaje).strip()
                    try:
                        return datetime.strptime(fecha, "%Y-%m-%d").date()
                    except ValueError:
                        print("⚠️ Formato inválido. Usa YYYY-MM-DD.")

            fecha_inicio = validar_fecha("Fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = validar_fecha("Fecha de fin (YYYY-MM-DD): ")

            if fecha_fin < fecha_inicio:
                print("⚠️ La fecha de fin no puede ser anterior a la de inicio.")
                continue

            # Motivo
            motivo = input("Motivo de la multa: ").strip().title()

            # Monto
            while True:
                monto = input("Monto de la multa: ").strip()
                if not monto.isdigit() or int(monto) <= 0:
                    print("⚠️ Ingrese un monto válido (mayor a 0).")
                else:
                    break

            agregar_multa(id_multa, id_cliente, id_renta, fecha_inicio.strftime("%Y-%m-%d"),
                        fecha_fin.strftime("%Y-%m-%d"), motivo, int(monto))



        elif opc == "2":
            mostrar_multas()

        elif opc == "3":
            print("\n✏️ Editar Multa Existente")

            id_multa = input("Ingrese el ID de la multa a editar: ").strip()
            if not id_multa.isdigit() or not id_existe("Multa", "ID_Multa", id_multa):
                print("❌ No existe una multa con ese ID.")
                continue

            # 🔍 Obtener ID_Cliente e ID_Renta actuales desde la base de datos
            try:
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("SELECT ID_Cliente, ID_Renta FROM Multa WHERE ID_Multa = %s", (id_multa,))
                resultado = cursor.fetchone()
                if resultado:
                    id_cliente, id_renta = resultado
                else:
                    print("❌ No se pudo recuperar los datos de la multa.")
                    return
            except mysql.connector.Error as err:
                print(f"❌ Error al recuperar información de la multa: {err}")
                return
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            # Validar fechas
            def validar_fecha(mensaje):
                while True:
                    fecha = input(mensaje).strip()
                    try:
                        return datetime.strptime(fecha, "%Y-%m-%d").date()
                    except ValueError:
                        print("⚠️ Formato inválido. Usa YYYY-MM-DD.")

            while True:
                fecha_inicio = validar_fecha("Nueva Fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = validar_fecha("Nueva Fecha de fin (YYYY-MM-DD): ")
                if fecha_fin < fecha_inicio:
                    print("⚠️ La fecha de fin no puede ser anterior a la de inicio.")
                else:
                    break

            motivo = input("Nuevo motivo de la multa: ").strip().title()

            while True:
                monto = input("Nuevo monto de la multa: ").strip()
                if not monto.isdigit() or int(monto) <= 0:
                    print("⚠️ Ingrese un monto válido.")
                else:
                    break

            actualizar_multa(id_multa, id_cliente, id_renta,
                             fecha_inicio.strftime("%Y-%m-%d"),
                             fecha_fin.strftime("%Y-%m-%d"),
                             motivo, int(monto))

        elif opc == "4":
            print("\n🗑️ Eliminar Multa")
            id_multa = input("Ingrese el ID de la multa a eliminar: ").strip()
            if not id_multa.isdigit():
                print("⚠️ El ID debe ser numérico.")
                continue
            if not id_existe("Multa", "ID_Multa", id_multa):
                print("⚠️ No existe una multa con ese ID.")
                continue

            try:
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT C.nombre_completo 
                    FROM Multa M
                    JOIN Cliente C ON M.ID_Cliente = C.ID_Cliente
                    WHERE M.ID_Multa = %s
                """, (id_multa,))
                resultado = cursor.fetchone()
                if resultado:
                    nombre_cliente = resultado[0]
                else:
                    print("❌ No se pudo encontrar el cliente asociado a esta multa.")
                    continue
            except Exception as e:
                print(f"❌ Error al consultar el cliente: {e}")
                continue
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            confirmacion = input(f"¿Está seguro que desea eliminar la multa asociada a {nombre_cliente}? (s/n): ").strip().lower()
            if confirmacion == "s":
                eliminar_multa(id_multa)
            else:
                print("❌ Operación cancelada por el usuario.")


        elif opc == "0":
            print("Saliendo del menú de Multas...")
            break

        else:
            print("⚠️ Opción no válida. Intente nuevamente.")


def transacciones():
    while True:
        print("\n¿Qué deseas hacer en Transacciones?")
        print("1️⃣  Añadir Transacción")
        print("2️⃣  Mostrar todas las Transacciones")
        print("3️⃣  Editar Transacción")
        print("4️⃣  Eliminar Transacción")
        print("0️⃣  Salir")
        print("-" * 50)

        opc = input("Seleccione una opción: ")

        if opc == "1":
            print("\n🆕 Ingreso de nueva transacción")

            # ID de la transacción
            while True:
                id_transaccion = input("ID de la transacción: ").strip()
                if not id_transaccion.isdigit():
                    print("⚠️ El ID debe ser numérico.")
                    continue
                if id_existe("Transaccion", "ID", id_transaccion):
                    print("⚠️ Ese ID ya existe.")
                    continue
                break

            # Validar ID Cliente
            while True:
                id_cliente = input("ID del Cliente: ").strip()
                if not id_cliente.isdigit() or not id_existe("Cliente", "ID_Cliente", id_cliente):
                    print("⚠️ Cliente no válido.")
                    continue

                try:
                    conn = obtener_conexion()
                    cursor = conn.cursor()
                    cursor.execute("SELECT nombre_completo FROM Cliente WHERE ID_Cliente = %s", (id_cliente,))
                    cliente = cursor.fetchone()
                    if cliente:
                        print(f"➡️ Cliente encontrado: {cliente[0]}")
                        confirmar = input("¿Desea continuar con este cliente? (s/n): ").strip().lower()
                        if confirmar == "s":
                            break
                    else:
                        print("❌ Cliente no encontrado.")
                except Exception as e:
                    print(f"❌ Error: {e}")
                finally:
                    if 'cursor' in locals(): cursor.close()
                    if 'conn' in locals(): conn.close()

            # Validar ID Renta
            while True:
                id_renta = input("ID de la Renta asociada: ").strip()
                if not id_renta.isdigit() or not id_existe("Renta", "ID_Renta", id_renta):
                    print("⚠️ Renta no válida.")
                    continue

                try:
                    conn = obtener_conexion()
                    cursor = conn.cursor()
                    cursor.execute("SELECT Tipo FROM Renta WHERE ID_Renta = %s", (id_renta,))
                    tipo = cursor.fetchone()
                    if tipo:
                        print(f"➡️ Tipo de renta: {tipo[0]}")
                        confirmar = input("¿Desea continuar con esta renta? (s/n): ").strip().lower()
                        if confirmar == "s":
                            break
                    else:
                        print("❌ Renta no encontrada.")
                except Exception as e:
                    print(f"❌ Error: {e}")
                finally:
                    if 'cursor' in locals(): cursor.close()
                    if 'conn' in locals(): conn.close()

            # Fecha
            while True:
                fecha = input("Fecha (YYYY-MM-DD): ").strip()
                try:
                    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("⚠️ Fecha inválida. Formato correcto: YYYY-MM-DD.")

            #Hora
            # Validar hora
            while True:
                hora_transaccion = input("Nueva Hora transacción (HHMM): ").strip()
                if not hora_transaccion.isdigit() or len(hora_transaccion) != 4:
                    print("⚠️ Hora inválida.")
                else:
                    break
            # Monto total
            while True:
                monto = input("Monto total de la transacción: ").strip()
                if not monto.isdigit() or int(monto) <= 0:
                    print("⚠️ Ingrese un monto válido (mayor a 0).")
                else:
                    break

            agregar_transaccion(id_transaccion, id_cliente, id_renta, fecha, hora_transaccion, int(monto))

        elif opc == "2":
            mostrar_transacciones()

        elif opc == "3":
            print("\n✏️ Editar transacción existente")

            id_transaccion = input("ID de la transacción a editar: ").strip()
            if not id_transaccion.isdigit() or not id_existe("Transaccion", "ID", id_transaccion):
                print("❌ No existe una transacción con ese ID.")
                continue

            try:
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("SELECT ID_Cliente, ID_Renta FROM Transaccion WHERE ID = %s", (id_transaccion,))
                resultado = cursor.fetchone()
                if resultado:
                    id_cliente, id_renta = resultado
                else:
                    print("❌ No se pudo recuperar los datos de la transacción.")
                    continue
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            # Fecha
            while True:
                fecha = input("Nueva fecha (YYYY-MM-DD): ").strip()
                try:
                    datetime.strptime(fecha, "%Y-%m-%d")
                    break
                except ValueError:
                    print("⚠️ Fecha inválida. Usa el formato YYYY-MM-DD.")

            # Hora
            # Validar hora
            while True:
                hora = input("Nueva Hora transacción (HHMM): ").strip()
                if not hora.isdigit() or len(hora) != 4:
                    print("⚠️ Hora inválida.")
                else:
                    break

            # Monto
            while True:
                monto = input("Nuevo monto total: ").strip()
                if not monto.isdigit() or int(monto) <= 0:
                    print("⚠️ Ingrese un monto válido.")
                else:
                    break

            actualizar_transaccion(id_transaccion, id_cliente, id_renta, fecha, hora, int(monto))

        elif opc == "4":
            print("\n🗑️ Eliminar transacción")
            id_transaccion = input("Ingrese el ID de la transacción a eliminar: ").strip()
            if not id_transaccion.isdigit():
                print("⚠️ El ID debe ser numérico.")
                continue
            if not id_existe("Transaccion", "ID", id_transaccion):
                print("⚠️ No existe una transacción con ese ID.")
                continue

            try:
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT C.nombre_completo 
                    FROM Transaccion T 
                    JOIN Cliente C ON T.ID_Cliente = C.ID_Cliente 
                    WHERE T.ID = %s
                """, (id_transaccion,))
                resultado = cursor.fetchone()
                if resultado:
                    nombre_cliente = resultado[0]
                else:
                    print("❌ No se pudo encontrar el cliente asociado a esta transacción.")
                    continue
            except Exception as e:
                print(f"❌ Error al consultar el cliente: {e}")
                continue
            finally:
                if 'cursor' in locals(): cursor.close()
                if 'conn' in locals(): conn.close()

            confirmacion = input(f"¿Está seguro que desea eliminar la transacción asociada a {nombre_cliente}? (s/n): ").strip().lower()
            if confirmacion == "s":
                eliminar_transaccion(id_transaccion)
            else:
                print("❌ Operación cancelada.")


        elif opc == "0":
            print("Saliendo del menú de Transacciones...")
            break

        else:
            print("⚠️ Opción no válida. Intente nuevamente.")