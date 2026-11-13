import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Misma paleta que la pantalla de acceso (Lab 8).
COLOR_FONDO = "#14213D"
COLOR_TEXTO = "#E5E5E5"
COLOR_ACENTO = "#FCA311"
COLOR_BORDE = "#2B3A67"
COLOR_EXPORTAR = "#2EC4B6"


class HomeView:
    """Pantalla principal: tabla de productos, formulario y exportación.

    Solo dibuja y lee widgets. No contiene lógica de archivos: el controlador
    decide qué hacer con el formato elegido y con la ruta del diálogo.
    """

    def __init__(self, root, nombre_usuario, formatos):
        self.root = root
        self.ventana = tk.Toplevel(root)
        self.ventana.title("Mi Sistema | Productos")

        ancho, alto = 860, 680
        x = (self.ventana.winfo_screenwidth() - ancho) // 2
        y = (self.ventana.winfo_screenheight() - alto) // 2
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.ventana.minsize(760, 600)
        self.ventana.configure(bg=COLOR_FONDO)

        self._crear_encabezado(nombre_usuario)
        self._crear_tabla()
        self._crear_formulario()
        self._crear_exportacion(formatos)

    # ------------------------------------------------------------------ UI
    def _crear_encabezado(self, nombre_usuario):
        marco = tk.Frame(self.ventana, bg=COLOR_FONDO)
        marco.pack(fill="x", padx=25, pady=(20, 10))

        textos = tk.Frame(marco, bg=COLOR_FONDO)
        textos.pack(side="left")

        tk.Label(
            textos, text="PRODUCTOS", font=("Arial", 22, "bold"),
            bg=COLOR_FONDO, fg=COLOR_ACENTO
        ).pack(anchor="w")

        tk.Label(
            textos, text=f"Usuario activo: {nombre_usuario}", font=("Arial", 10),
            bg=COLOR_FONDO, fg=COLOR_TEXTO
        ).pack(anchor="w")

        self.btn_cerrar_sesion = tk.Button(
            marco, text="Cerrar sesión", bg=COLOR_BORDE, fg="white",
            activebackground="#3A4B80", activeforeground="white",
            relief="flat", padx=12, pady=4, cursor="hand2"
        )
        self.btn_cerrar_sesion.pack(side="right")

    def _crear_tabla(self):
        marco = tk.LabelFrame(
            self.ventana, text="Productos registrados",
            font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO
        )
        marco.pack(fill="both", expand=True, padx=25, pady=5)

        self.tabla = ttk.Treeview(
            marco, columns=("id", "nombre", "precio", "stock"),
            show="headings", height=8
        )
        self.tabla.heading("id", text="id")
        self.tabla.heading("nombre", text="nombre")
        self.tabla.heading("precio", text="precio")
        self.tabla.heading("stock", text="stock")
        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("nombre", width=320, anchor="w")
        self.tabla.column("precio", width=120, anchor="e")
        self.tabla.column("stock", width=80, anchor="e")

        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll.pack(side="right", fill="y", padx=(0, 8), pady=8)

    def _crear_formulario(self):
        marco = tk.LabelFrame(
            self.ventana, text="Agregar producto",
            font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO
        )
        marco.pack(fill="x", padx=25, pady=5)

        estilo_etiqueta = {"bg": COLOR_FONDO, "fg": COLOR_TEXTO}
        estilo_campo = {
            "relief": "flat", "highlightthickness": 2,
            "highlightbackground": COLOR_BORDE, "highlightcolor": COLOR_ACENTO
        }

        tk.Label(marco, text="Nombre:", **estilo_etiqueta).grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.entry_nombre = tk.Entry(marco, width=28, **estilo_campo)
        self.entry_nombre.grid(row=0, column=1, padx=4, pady=8, ipady=2)

        tk.Label(marco, text="Precio:", **estilo_etiqueta).grid(row=0, column=2, padx=8, pady=8, sticky="e")
        self.entry_precio = tk.Entry(marco, width=10, **estilo_campo)
        self.entry_precio.grid(row=0, column=3, padx=4, pady=8, ipady=2)

        tk.Label(marco, text="Stock:", **estilo_etiqueta).grid(row=0, column=4, padx=8, pady=8, sticky="e")
        self.entry_stock = tk.Entry(marco, width=8, **estilo_campo)
        self.entry_stock.grid(row=0, column=5, padx=4, pady=8, ipady=2)

        self.btn_guardar = tk.Button(
            marco, text="Guardar", bg=COLOR_ACENTO, fg=COLOR_FONDO,
            activebackground="#E39200", activeforeground=COLOR_FONDO,
            font=("Arial", 10, "bold"), relief="flat", padx=14, pady=3, cursor="hand2"
        )
        self.btn_guardar.grid(row=1, column=0, columnspan=6, padx=12, pady=(0, 10), sticky="e")

    def _crear_exportacion(self, formatos):
        marco = tk.LabelFrame(
            self.ventana, text="Exportar productos",
            font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO
        )
        marco.pack(fill="x", padx=25, pady=(5, 20))

        tk.Label(
            marco, text="Formato:", bg=COLOR_FONDO, fg=COLOR_TEXTO
        ).pack(side="left", padx=(12, 6), pady=14)

        # Menú desplegable de solo lectura: CSV, TXT, JSON, PDF.
        self.combo_formato = ttk.Combobox(
            marco, values=list(formatos), state="readonly", width=10
        )
        self.combo_formato.current(0)
        self.combo_formato.pack(side="left", padx=(0, 16), pady=14)

        self.btn_exportar = tk.Button(
            marco, text="Exportar Reporte", width=18,
            bg=COLOR_EXPORTAR, fg=COLOR_FONDO,
            activebackground="#25A99D", activeforeground=COLOR_FONDO,
            font=("Arial", 10, "bold"), relief="flat", pady=5, cursor="hand2"
        )
        self.btn_exportar.pack(side="left", pady=14)

    # ------------------------------------------------- métodos para el controlador
    def cargar_tabla(self, productos):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for p in productos:
            self.tabla.insert(
                "", "end",
                values=(p["id"], p["nombre"], f"{p['precio']:.2f}", p["stock"])
            )

    def obtener_datos_formulario(self):
        return (
            self.entry_nombre.get().strip(),
            self.entry_precio.get().strip(),
            self.entry_stock.get().strip(),
        )

    def limpiar_formulario(self):
        for entrada in (self.entry_nombre, self.entry_precio, self.entry_stock):
            entrada.delete(0, tk.END)

    def obtener_formato(self):
        """Formato elegido en el Combobox: "CSV", "TXT", "JSON" o "PDF"."""
        return self.combo_formato.get()

    def pedir_ruta_guardado(self, extension, descripcion):
        """Cuadro de diálogo "Guardar como". Devuelve la ruta o "" si se cancela."""
        ruta = filedialog.asksaveasfilename(
            parent=self.ventana,
            title="Guardar exportación",
            initialfile="productos",
            defaultextension=extension,
            filetypes=[(descripcion, f"*{extension}"), ("Todos los archivos", "*.*")]
        )
        return ruta or ""

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror(titulo, mensaje, parent=self.ventana)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje, parent=self.ventana)
        else:
            messagebox.showinfo(titulo, mensaje, parent=self.ventana)

    def cerrar(self):
        self.ventana.destroy()
