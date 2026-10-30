import tkinter as tk

from controllers.authentication_controller import Authentication
from models.user_model import UserModel
from views.login_view import LoginView


def main():
    root = tk.Tk()

    modelo = UserModel()                           # Modelo: acceso a la base de datos
    vista = LoginView(root)                        # Vista: pantalla de inicio de sesión
    controlador = Authentication(modelo, vista)    # Controlador: conecta modelo y vistas

    root.mainloop()


if __name__ == "__main__":
    main()
