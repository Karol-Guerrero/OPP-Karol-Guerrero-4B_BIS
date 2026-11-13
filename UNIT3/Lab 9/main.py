import tkinter as tk

from controllers.authentication_controller import Authentication
from controllers.products_controller import ProductsController
from exporters import EXPORTERS
from models.products_model import Producto
from models.user_model import UserModel
from views.home_view import HomeView
from views.login_view import LoginView


def main():
    root = tk.Tk()

    modelo_usuarios = UserModel()       # Modelo: usuarios
    vista_login = LoginView(root)       # Vista: inicio de sesión

    def abrir_inicio(nombre_usuario):
        """Login correcto: oculta el login y muestra la pantalla de productos."""
        root.withdraw()
        vista_inicio = HomeView(root, nombre_usuario, EXPORTERS)

        def volver_al_login():
            vista_inicio.cerrar()
            root.deiconify()

        ProductsController(
            Producto(),                                # Modelo: productos
            vista_inicio,                              # Vista: pantalla principal
            al_cerrar_sesion=volver_al_login,
            al_salir=controlador_login.cerrar_aplicacion,
        )

    # Controlador: conecta el login con el modelo y abre la pantalla principal
    controlador_login = Authentication(
        modelo_usuarios, vista_login, al_ingresar=abrir_inicio
    )

    root.mainloop()


if __name__ == "__main__":
    main()
