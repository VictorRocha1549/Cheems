import mysql.connector
from mysql.connector import Error

def get_dn_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='0801',
        database='cheems'
    )