import tkinter as tk
from tkinter import messagebox

# Paleta de la pantalla de acceso (puedes cambiar estos colores a tu gusto).
COLOR_FONDO = "#14213D"
COLOR_TEXTO = "#E5E5E5"
COLOR_ACENTO = "#FCA311"
COLOR_BORDE = "#2B3A67"


class LoginView:

    def __init__(self, root):
        self.root = root

        # PERSONALIZAR 1 (hecho):
        # Cambia el título de la ventana.
        self.root.title("Mi Sistema | Acceso")

        # PERSONALIZAR 2 (hecho):
        # Modifica el ancho y alto de la ventana (además se centra en la pantalla).
        ancho, alto = 460, 490
        x = (self.root.winfo_screenwidth() - ancho) // 2
        y = (self.root.winfo_screenheight() - alto) // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        # PERSONALIZAR 3 (hecho):
        # Cambia el color de fondo.
        self.root.configure(bg=COLOR_FONDO)

        self.root.resizable(False, False)

        # PERSONALIZAR 4 (hecho):
        # Cambia el texto, la fuente y los colores del título.
        self.titulo = tk.Label(
            root,
            text="BIENVENIDO",
            font=("Arial", 26, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        )
        self.titulo.pack(pady=(40, 5))

        self.subtitulo = tk.Label(
            root,
            text="Inicia sesión para continuar",
            font=("Arial", 11),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        self.subtitulo.pack(pady=(0, 25))

        # PERSONALIZAR 5 (hecho):
        # Modifica el texto y la apariencia de las etiquetas.
        self.lbl_email = tk.Label(
            root,
            text="Correo electrónico",
            font=("Arial", 11, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        self.lbl_email.pack()

        # PERSONALIZAR 6 (hecho):
        # Cambia el ancho, la fuente y otros atributos del campo.
        self.entry_email = tk.Entry(
            root,
            width=30,
            font=("Arial", 12),
            relief="flat",
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_ACENTO
        )
        self.entry_email.pack(pady=(5, 15), ipady=4)

        self.lbl_password = tk.Label(
            root,
            text="Contraseña",
            font=("Arial", 11, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        self.lbl_password.pack()

        # El atributo show oculta los caracteres al escribir.
        self.entry_password = tk.Entry(
            root,
            width=30,
            font=("Arial", 12),
            show="*",
            relief="flat",
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_ACENTO
        )
        self.entry_password.pack(pady=(5, 20), ipady=4)

        # PERSONALIZAR 7 (hecho):
        # Cambia el texto, color, tamaño y fuente del botón.
        self.btn_login = tk.Button(
            root,
            text="Iniciar sesión",
            width=24,
            bg=COLOR_ACENTO,
            fg=COLOR_FONDO,
            activebackground="#E39200",
            activeforeground=COLOR_FONDO,
            font=("Arial", 12, "bold"),
            relief="flat",
            pady=6,
            cursor="hand2"
        )
        self.btn_login.pack(pady=(5, 15))

        # PERSONALIZAR 8 (hecho):
        # Cambia el diseño del botón para abrir el registro.
        self.btn_register = tk.Button(
            root,
            text="¿No tienes cuenta? Regístrate",
            width=28,
            bg=COLOR_BORDE,
            fg="white",
            activebackground="#3A4B80",
            activeforeground="white",
            font=("Arial", 10),
            relief="flat",
            pady=4,
            cursor="hand2"
        )
        self.btn_register.pack()

    def obtener_datos(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get()

        return email, password

    def limpiar_campos(self):
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror(titulo, mensaje, parent=self.root)
        else:
            messagebox.showinfo(titulo, mensaje, parent=self.root)
