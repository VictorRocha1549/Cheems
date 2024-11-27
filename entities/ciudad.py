from persistences.db import get_dn_connection
from mysql.connector import Error

class Ciudad:
    def __init__(self, nombre, codigo):
        self.nombre = nombre
        self.codigo = codigo
    
    @classmethod
    def get_all(cls):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM ciudad')
            return cursor.fetchall()
        except Error as e:
            return str(e)
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_id(ciudad_id):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM ciudad WHERE id = %s', (ciudad_id,))
            ciudad = cursor.fetchone()  # Obtener el primer resultado
            return ciudad  # Devuelve el diccionario con los datos de la ciudad
        except Error as e:
            print(f"Error al obtener ciudad por ID: {e}")  # Depuración en caso de error
            return None
        finally:
            cursor.close()
            connection.close()
    
    @classmethod
    def save(cls, ciudad):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO ciudad(nombre, codigo) VALUES(%s,%s)', (ciudad.nombre, ciudad.codigo))
            connection.commit()
            return cursor.lastrowid  # Devuelve el ID de la ciudad recién insertada
        except Error as e:
            return str(e)
        finally:
            cursor.close()
            connection.close()
    
    @classmethod
    def update(cls, id, ciudad):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor()
            cursor.execute('UPDATE ciudad SET nombre = %s, codigo = %s WHERE id = %s', 
                           (ciudad.nombre, ciudad.codigo, id))
            connection.commit()
            return cursor.rowcount  # Devuelve el número de filas afectadas
        except Error as e:
            return str(e)
        finally:
            cursor.close()
            connection.close()