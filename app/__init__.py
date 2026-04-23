from flask import Flask
import mysql.connector
from mysql.connector import pooling

app = Flask(__name__)
app.secret_key = 'Tu_Clave_Secreta_Va_Aqui'  # Cambia esto por una clave secreta segura 

# Configure MySQL connection pool
dbconfig = {
    "database"  : "estacionamiento_db",
    "user"      : "root",
    "password"  : "Tu_Contraseña_De_MySQL_Va_Aqui", # Pon aquí la contraseña de tu MySQL
    "host"      : "localhost"
}

db_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                      pool_size=5,
                                                      **dbconfig
)

def get_db_connection():
    return db_pool.get_connection()

from app import routes, auth
