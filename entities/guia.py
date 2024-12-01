from persistences.db import get_dn_connection
from mysql.connector import Error

class Guia:
    def __init__(self, id=None, fecha='', estado='', ciudad_id='', envio_numero_guia=''):
        self.id=id
        self.fecha=fecha
        self.estado=estado
        self.ciudad_id=ciudad_id
        self.envio_numero_guia=envio_numero_guia

    @staticmethod
    def get_all(cls):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM puntos')
            return cursor.fetchall()
        except Error as e:
            return str(e)
        finally:
            cursor.close()
            connection.close()
        
    @staticmethod
    def get_by_id(guia_id):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM punto WHERE id= %s',(guia_id))
            guia = cursor.fetchone()
            return guia
        except Error as e:
            print(f"Error al obtener guia por ID: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    