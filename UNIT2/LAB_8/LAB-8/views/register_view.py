import tkinter as tk
from tkinter import messagebox

# Paleta de la pantalla de registro (puedes cambiar estos colores a tu gusto).
COLOR_FONDO = "#0B132B"
COLOR_TEXTO = "#E5E5E5"
COLOR_ACENTO = "#2EC4B6"
COLOR_BORDE = "#1C2541"


class RegisterView:

    def __init__(self, root):
        self.ventana = tk.Toplevel(root)

        # PERSONALIZAR 1 (hecho):
        # Cambia el título de la ventana.
        self.ventana.title("Mi Sistema | Crear cuenta")

        # PERSONALIZAR 2 (hecho):
        # Modifica las dimensiones de la ventana (además se centra en la pantalla).
        ancho, alto = 460, 530
        x = (self.ventana.winfo_screenwidth() - ancho) // 2
        y = (self.ventana.winfo_screenheight() - alto) // 2
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        # PERSONALIZAR 3 (hecho):
        # Cambia el color de fondo.
        self.ventana.configure(bg=COLOR_FONDO)

        self.ventana.resizable(False, False)

        # Mantiene la ventana asociada a la principal.
        self.ventana.transient(root)
        # Espera a que la ventana sea visible: en algunos sistemas grab_set()
        # falla con "window not viewable" si se llama antes.
        self.ventana.wait_visibility()
        self.ventana.grab_set()

        # PERSONALIZAR 4 (hecho):
        # Cambia el título, la fuente y sus colores.
        self.titulo = tk.Label(
            self.ventana,
            text="CREAR CUENTA",
            font=("Arial", 24, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        )
        self.titulo.pack(pady=(30, 20))

        # PERSONALIZAR 5 (hecho):
        # Modifica el texto y estilo de las etiquetas.
        self.lbl_nombre = tk.Label(
            self.ventana,
            text="Nombre completo",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=("Arial", 10, "bold")
        )
        self.lbl_nombre.pack()

        self.entry_nombre = tk.Entry(
            self.ventana,
            width=32,
            font=("Arial", 11),
            relief="flat",
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_ACENTO
        )
        self.entry_nombre.pack(pady=(4, 10), ipady=3)

        self.lbl_email = tk.Label(
            self.ventana,
            text="Correo electrónico",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=("Arial", 10, "bold")
        )
        self.lbl_email.pack()

        self.entry_email = tk.Entry(
            self.ventana,
            width=32,
            font=("Arial", 11),
            relief="flat",
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_ACENTO
        )
        self.entry_email.pack(pady=(4, 10), ipady=3)

        self.lbl_password = tk.Label(
            self.ventana,
            text="Contraseña",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=("Arial", 10, "bold")
        )
        self.lbl_password.pack()

        self.entry_password = tk.Entry(
            self.ventana,
            width=32,
            show="*",
            font=("Arial", 11),
            relief="flat",
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_ACENTO
        )
        self.entry_password.pack(pady=(4, 10), ipady=3)

        self.lbl_confirmar = tk.Label(
            self.ventana,
            text="Confirmar contraseña",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=("Arial", 10, "bold")
        )
        self.lbl_confirmar.pack()

        self.entry_confirmar = tk.Entry(
            self.ventana,
            width=32,
            show="*",
            font=("Arial", 11),
            relief="flat",
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_ACENTO
        )
        self.entry_confirmar.pack(pady=(4, 10), ipady=3)

        # PERSONALIZAR 6 (hecho):
        # Cambia el texto, color, fuente y tamaño del botón.
        self.btn_guardar = tk.Button(
            self.ventana,
            text="Registrar usuario",
            width=26,
            bg=COLOR_ACENTO,
            fg=COLOR_FONDO,
            activebackground="#25A99D",
            activeforeground=COLOR_FONDO,
            font=("Arial", 11, "bold"),
            relief="flat",
            pady=5,
            cursor="hand2"
        )
        self.btn_guardar.pack(pady=(15, 8))

        # Botón para cancelar el registro.
        self.btn_cancelar = tk.Button(
            self.ventana,
            text="Cancelar",
            width=26,
            bg=COLOR_BORDE,
            fg="white",
            activebackground="#2B3A67",
            activeforeground="white",
            relief="flat",
            pady=3,
            command=self.cerrar,
            cursor="hand2"
        )
        self.btn_cancelar.pack()

        self.entry_nombre.focus_set()

    def obtener_datos(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        confirmar = self.entry_confirmar.get()

        return nombre, email, password, confirmar

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror(
                titulo,
                mensaje,
                parent=self.ventana
            )
        else:
            messagebox.showinfo(
                titulo,
                mensaje,
                parent=self.ventana
            )

    def cerrar(self):
        self.ventana.destroy()
