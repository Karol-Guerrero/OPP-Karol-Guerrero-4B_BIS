import mysql.connector

from controllers.conexion_controller import Conexion


class Producto:

    def __init__(self, id=None, nombre=None, precio=None, stock=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.conexion_db = Conexion()

    def obtener_todos(self):
        """Lista de diccionarios con todos los productos (None si hay un error)."""
        conexion = self.conexion_db.conectar()

        if conexion is None:
            return None

        cursor = None

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, nombre, precio, stock FROM productos ORDER BY id"
            )
            return cursor.fetchall()

        except mysql.connector.Error as error:
            print("Error al consultar productos:", error)
            return None

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def guardar(self):
        """Inserta este producto en la base de datos. Retorna True si se guardó."""
        conexion = self.conexion_db.conectar()

        if conexion is None:
            return False

        cursor = None

        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                (self.nombre, self.precio, self.stock)
            )
            conexion.commit()
            return True

        except mysql.connector.Error as error:
            print("Error al guardar el producto:", error)
            return False

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()
