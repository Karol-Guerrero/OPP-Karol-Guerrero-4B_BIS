from Controller.database_connection import Database_connection


class Producto:
    def __init__(self, id=None, nombre=None, precio=None, stock=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.db = Database_connection()

    def obtener_todos(self):
        """Retorna una lista con todos los productos registrados (None si hay error)."""
        query = "SELECT id, nombre, precio, stock FROM productos ORDER BY id"
        return self.db.ejecutar_consulta(query)

    def guardar(self):
        """Inserta un nuevo producto en la base de datos. Retorna True si se guardó."""
        query = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
        filas = self.db.ejecutar_consulta(query, (self.nombre, self.precio, self.stock))
        return filas is not None and filas > 0
