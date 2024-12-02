from persistences.db import get_dn_connection
from mysql.connector import Error

class Guia:
    def __init__(self, id=None, fecha='', estado='', ciudad_id='', envio_numero_guia=''):
        self.id = id
        self.fecha = fecha
        self.estado = estado
        self.ciudad_id = ciudad_id
        self.envio_numero_guia = envio_numero_guia

    @staticmethod
    def get_all():
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM puntos')  # Usamos la tabla 'puntos'
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
            cursor.execute('SELECT * FROM puntos WHERE id = %s', (guia_id,))
            guia = cursor.fetchone()
            return guia
        except Error as e:
            print(f"Error al obtener guia por ID: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_by_numero_guia(numero_guia):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM puntos WHERE envio_numero_guia = %s', (numero_guia,))
            envio_data = cursor.fetchone()
            if envio_data:
                # Retornar una instancia de Guia con los datos obtenidos
                return Guia(**envio_data)
            else:
                return None
        except Error as e:
            print(f"Error al obtener envío por número de guía: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
            