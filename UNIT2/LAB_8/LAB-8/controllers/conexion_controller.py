import os

import mysql.connector


class Conexion:
    """Controlador de la conexión a MySQL / MariaDB (XAMPP)."""

    def __init__(self):
        # Valores por defecto de XAMPP: usuario root, sin contraseña y puerto 3306.
        # Se pueden cambiar con variables de entorno (misma idea que en el lab 7).
        self.host = os.getenv("DB_HOST", "localhost")
        self.puerto = int(os.getenv("DB_PORT", "3306"))
        self.usuario = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.base_datos = os.getenv("DB_NAME", "login_mvc")

    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                port=self.puerto,
                user=self.usuario,
                password=self.password,
                database=self.base_datos,
                charset="utf8mb4"
            )
            return conexion

        except mysql.connector.Error as error:
            print("Error al conectar con MySQL:", error)
            return None


if __name__ == "__main__":
    # Prueba rápida de la conexión:  python controllers/conexion_controller.py
    prueba = Conexion().conectar()

    if prueba is not None:
        print("Conexión exitosa a la base de datos:", prueba.database)
        prueba.close()
    else:
        print("No se pudo conectar. Revisa que MySQL esté iniciado en XAMPP "
              "y que la base login_mvc exista.")
