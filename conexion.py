import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        user = 'root',       # ingrese nombre del usuario
        password = 'admin',   # ingrese contraseña de su servidor
        host = 'localhost',       # ingrese nombre del servidor
        database = 'svrp',   # ingrese nombre de la base de datos
        port = 3306        # ingrese el puerto, por defecto es el 3306
    )