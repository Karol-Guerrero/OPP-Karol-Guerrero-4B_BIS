import mysql.connector
from mysql.connector import Error

from Controller.config import DB_CONFIG


class Database_connection:
    def __init__(self):
        self.config = DB_CONFIG

    def obtener_conexion(self):
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return None

    def ejecutar_consulta(self, query, params=()):
        """
        SELECT -> lista de diccionarios (puede ser lista vacía).
        INSERT / UPDATE / DELETE -> número de filas afectadas (con commit).
        Si hay un error de conexión o de SQL -> None.
        """
        conexion = self.obtener_conexion()
        if conexion is None:
            return None

        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(query, params)
            if cursor.with_rows:
                return cursor.fetchall()
            conexion.commit()
            return cursor.rowcount
        except Error as e:
            conexion.rollback()
            print(f"Error en la consulta SQL: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()
