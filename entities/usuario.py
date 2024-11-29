from persistences.db import get_dn_connection
from mysql.connector import Error


class Usuario:
    def __init__(self, nombre, contrasenia, ciudad_id):
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.ciudad_id = ciudad_id

    @classmethod
    def get_all(cls):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM usuarios')
            return cursor.fetchall()
        except Error as e:
            return str(e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_by_id(usuario_id):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM usuarios WHERE id = %s', (usuario_id,))
            ciudad = cursor.fetchone()  
            return ciudad  
        except Error as e:
            print(f"Error al obtener ciudad por ID: {e}") 
            return None
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def save(cls, usuario):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO usuarios(nombre, contrasenia, ciudad_id) VALUES(%s,%s,%s)', (usuario.nombre, usuario.contrasenia, usuario.ciudad_id))
            connection.commit()
            return cursor.lastrowid  # Devuelve el ID de la ciudad recién insertada
        except Error as e:
            return str(e)
        finally:
            cursor.close()
            connection.close()

    