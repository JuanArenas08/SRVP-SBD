import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        user = 'root',       # ingrese nombre del usuario
        password = 'asdasd',   # ingrese contraseña de su servidor
        host = '127.0.0.1',       # ingrese nombre del servidor
        database = 'srvp',   # ingrese nombre de la base de datos
        port = 3306        # ingrese el puerto, por defecto es el 3306
    )