import mysql.connector
from mysql.connector import Error

def get_dn_connection():
    return mysql.connector.connect(
        host='162.241.2.39',
        user='itsonapp_244277',
        password='244277db#563G',
        database='itsonapp_244277'
    )