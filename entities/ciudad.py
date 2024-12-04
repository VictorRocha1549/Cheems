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
            cursor.execute('SELECT * FROM ciudad WHERE id = %s', (id,))
            existing_city = cursor.fetchone()
            if existing_city is None:
                print(f"No se encontró una ciudad con el id: {id}")
                return 0  # No se encontró la ciudad, no se puede actualizar
        
            cursor.execute('UPDATE ciudad SET nombre = %s, codigo = %s WHERE id = %s', 
                            (ciudad.nombre, ciudad.codigo, id))
            connection.commit()
            print(f"Filas afectadas por la actualización: {cursor.rowcount}")
            return cursor.rowcount  # 1 si se actualizó correctamente
        except Error as e:
            print(f"Error al actualizar la ciudad: {e}")
            return str(e)
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_by_name(ciudad_nombre):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM ciudad WHERE nombre = %s', (ciudad_nombre,))
            ciudad = cursor.fetchone()  # Obtener el primer resultado
            return ciudad  # Devuelve el diccionario con los datos de la ciudad
        except Error as e:
            print(f"Error al obtener ciudad por nombre: {e}")  # Depuración en caso de error
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete(ciudad_id):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor()
            cursor.execute('DELETE FROM ciudad WHERE id = %s', (ciudad_id,))
            connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error al eliminar la ciudad: {e}")
            return 0
        finally:
            cursor.close()
            connection.close()
