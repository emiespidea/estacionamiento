# Archivo: crear_admin.py
from werkzeug.security import generate_password_hash
import mysql.connector

# Conexión a tu base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tu_Contraseña_De_MySQL_Va_Aqui", # Pon aquí la contraseña de tu MySQL
    database="estacionamiento_db"
)
cursor = conexion.cursor()

# Datos de tu primer usuario
nombre = "Administrador Principal"
email = "admin@estacionamiento.com"
username = "admin"
password_plana = "admin123" # Esta es la que usarás para entrar
perfil = "admin"

# Encriptamos la contraseña
password_encriptada = generate_password_hash(password_plana)

try:
    consulta = """INSERT INTO Usuarios (nombre, email, username, password, perfil) 
                  VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(consulta, (nombre, email, username, password_encriptada, perfil))
    conexion.commit()
    print("¡Usuario administrador creado con éxito!")
    print(f"Tu usuario es: {username}")
    print(f"Tu contraseña es: {password_plana}")
except Exception as e:
    print(f"Error al crear usuario: {e}")
finally:
    cursor.close()
    conexion.close()

