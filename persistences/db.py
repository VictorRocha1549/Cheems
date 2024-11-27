import mysql.connector
from mysql.connector import Error

def get_dn_connection():
    try:
        connection = mysql.connector.connect(
            host='162.241.2.39',  
            user='itsonapp_244277', 
            password='244277db#563G',  
            database='itsonapp_244277' 
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error al conectar a la base de datos:", e)
        return None
