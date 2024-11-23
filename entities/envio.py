from persistences.db import get_dn_connection
import random
import string
import logging

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
        cursor.execute("SELECT * FROM envios") 
        envios_data = cursor.fetchall()
        cursor.close()
        conn.close()

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
            conn = get_dn_connection()
            cursor = conn.cursor()

            if not self.numero_guia:
                self.numero_guia = self.generar_numero_guia_unico()

            query = """
                INSERT INTO envios (origen_id, destino_id, remitente, destinatario, fecha_envio, numero_guia, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (self.origen_id, self.destino_id, self.remitente, self.destinatario,
                               self.fecha_envio, self.numero_guia, self.estado))

            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            logging.error(f"Error al intentar guardar el envío: {e}")
            return {"error": f"No se pudo crear el envío: {str(e)}"}

        return {"success": "Envío creado exitosamente"}

    @staticmethod
    def update(id, envio):
        conn = get_dn_connection()
        cursor = conn.cursor()

        if not envio.numero_guia:
            envio.numero_guia = None  

        query = """
        UPDATE envios
        SET origen_id = %s, destino_id = %s, remitente = %s, destinatario = %s,
            fecha_envio = %s, numero_guia = %s, estado = %s
        WHERE id = %s
        """
        cursor.execute(query, (envio.origen_id, envio.destino_id, envio.remitente, envio.destinatario,
                           envio.fecha_envio, envio.numero_guia, envio.estado, id))

        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
    
        return rows_affected

    @staticmethod
    def delete(id):

        conn = get_dn_connection()
        cursor = conn.cursor()

        query = "DELETE FROM envios WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected

    @staticmethod
    def generar_numero_guia_unico():
        while True:
            # Genera un número de guía aleatorio de 10 caracteres alfanuméricos (A12345BCDE)
            numero_guia = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

            conn = get_dn_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM envios WHERE numero_guia = %s", (numero_guia,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if not result:
                return numero_guia