from persistences.db import get_dn_connection
import random
import string
import logging
from mysql.connector import Error

class Envio:
    def __init__(self, id=None, origen_id='', destino_id='', remitente='', destinatario='', fecha_envio='', numero_guia='', estado=''):
        self.id = id
        self.origen_id = origen_id
        self.destino_id = destino_id
        self.remitente = remitente
        self.destinatario = destinatario
        self.fecha_envio = fecha_envio
        self.numero_guia = numero_guia
        self.estado = estado


    @staticmethod
    def get_all():
        conn = get_dn_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM envios")  # Asegúrate de que esta consulta devuelve todos los campos necesarios
        envios_data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convertir los resultados a objetos Envio, asegurando que la cantidad de campos coincida
        return [Envio(*envio_data) for envio_data in envios_data]

    @staticmethod
    def get_by_id(id):
        conn = get_dn_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM envios WHERE id = %s", (id,))
        envio_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if envio_data:
            return Envio(*envio_data)
        return None

    def save(self):
        try:
        # Crear una conexión con la base de datos
            conn = get_dn_connection()
            cursor = conn.cursor()

        # Si el número de guía no se proporciona, generar uno aleatorio de 10 dígitos
            if not self.numero_guia:
                self.numero_guia = self.generar_numero_guia_unico()

        # Insertar el nuevo envío en la base de datos
            query = """
                INSERT INTO envios (origen_id, destino_id, remitente, destinatario, fecha_envio, numero_guia, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (self.origen_id, self.destino_id, self.remitente, self.destinatario,
                               self.fecha_envio, self.numero_guia, self.estado))

        # Confirmar la transacción
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            logging.error(f"Error al intentar guardar el envío: {e}")
            return {"error": f"No se pudo crear el envío: {str(e)}"}

        return {"success": "Envío creado exitosamente"}

    @classmethod
    def update(cls, id, envio, numero_guia):
        try:
            connection = get_dn_connection()
            cursor = connection.cursor()
            cursor.execute('UPDATE envios SET origen_id = %s, destino_id = %s, remitente = %s, destinatario = %s, fecha_envio = %s, numero_guia = %s, estado = %s WHERE id = %s', 
                           (envio.origen_id, envio.destino_id, envio.remitente, envio.destinatario, envio.fecha_envio, numero_guia, envio.estado, id))
            connection.commit()
            return cursor.rowcount  # Devuelve el número de filas afectadas
        except Error as e:
            return str(e)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete(id):
        # Establecer conexión con la base de datos
        conn = get_dn_connection()
        cursor = conn.cursor()

        # Eliminar el envío
        query = "DELETE FROM envios WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()

        # Retornar el número de filas afectadas
        return rows_affected

    @staticmethod
    def generar_numero_guia_unico():
        while True:
            # Genera un número de guía aleatorio de 10 caracteres alfanuméricos (A12345BCDE)
            numero_guia = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            
            # Verificar si el número de guía ya existe en la base de datos
            conn = get_dn_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM envios WHERE numero_guia = %s", (numero_guia,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            # Si no se encuentra el número de guía en la base de datos, lo devolvemos
            if not result:
                return numero_guia