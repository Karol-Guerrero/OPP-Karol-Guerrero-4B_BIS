import tkinter as tk
from decimal import Decimal, InvalidOperation
from tkinter import ttk, messagebox

from Models.products_model import Producto


class DashboardVentana:
    def __init__(self, root, nombre_usuario):
        self.root = root
        self.root.title("Panel Principal")
        self.root.geometry("800x580")
        self.root.minsize(700, 520)

        self.producto = Producto()
        self._crear_interfaz(nombre_usuario)
        self.cargar_productos()

    def _crear_interfaz(self, nombre_usuario):
        lbl_mensaje = tk.Label(
            self.root,
            text=f"¡Bienvenido/a al Sistema!\nUsuario activo: {nombre_usuario}",
            font=("Helvetica", 12),
            justify="center",
        )
        lbl_mensaje.pack(pady=(15, 10))

        # --- Tabla de productos -------------------------------------------
        marco_tabla = tk.LabelFrame(
            self.root, text="Productos registrados", font=("Helvetica", 10, "bold")
        )
        marco_tabla.pack(fill="both", expand=True, padx=20, pady=5)

        columnas = ("id", "nombre", "precio", "stock")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=8)
        self.tabla.heading("id", text="id")
        self.tabla.heading("nombre", text="nombre")
        self.tabla.heading("precio", text="precio")
        self.tabla.heading("stock", text="stock")
        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("nombre", width=300, anchor="w")
        self.tabla.column("precio", width=120, anchor="e")
        self.tabla.column("stock", width=80, anchor="e")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll.pack(side="right", fill="y", padx=(0, 8), pady=8)

        # --- Formulario para agregar productos ----------------------------
        marco_form = tk.LabelFrame(
            self.root, text="Agregar producto", font=("Helvetica", 10, "bold")
        )
        marco_form.pack(fill="x", padx=20, pady=(5, 15))

        tk.Label(marco_form, text="Nombre:").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.entry_nombre = tk.Entry(marco_form, width=28)
        self.entry_nombre.grid(row=0, column=1, padx=4, pady=8)

        tk.Label(marco_form, text="Precio:").grid(row=0, column=2, padx=8, pady=8, sticky="e")
        self.entry_precio = tk.Entry(marco_form, width=10)
        self.entry_precio.grid(row=0, column=3, padx=4, pady=8)

        tk.Label(marco_form, text="Stock:").grid(row=0, column=4, padx=8, pady=8, sticky="e")
        self.entry_stock = tk.Entry(marco_form, width=8)
        self.entry_stock.grid(row=0, column=5, padx=4, pady=8)

        btn_guardar = tk.Button(
            marco_form, text="Guardar", command=self.guardar_producto,
            bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"), padx=12,
        )
        btn_guardar.grid(row=1, column=0, columnspan=6, padx=12, pady=(0, 10), sticky="e")

    def cargar_productos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = self.producto.obtener_todos()
        if productos is None:
            messagebox.showerror(
                "Error de conexión",
                "No se pudieron cargar los productos de la base de datos.",
            )
            return

        for p in productos:
            self.tabla.insert(
                "", "end", values=(p["id"], p["nombre"], f"{p['precio']:.2f}", p["stock"])
            )

    def guardar_producto(self):
        nombre = self.entry_nombre.get().strip()
        precio_txt = self.entry_precio.get().strip().replace(",", ".")
        stock_txt = self.entry_stock.get().strip()

        if not nombre or not precio_txt or not stock_txt:
            messagebox.showwarning("Campos vacíos", "Completa nombre, precio y stock.")
            return

        try:
            precio = Decimal(precio_txt)
            stock = int(stock_txt)
        except (InvalidOperation, ValueError):
            messagebox.showwarning(
                "Datos inválidos",
                "El precio debe ser un número (ej. 350.00) y el stock un número entero.",
            )
            return

        if not precio.is_finite() or precio < 0 or stock < 0:
            messagebox.showwarning("Datos inválidos", "El precio y el stock no pueden ser negativos.")
            return

        nuevo = Producto(nombre=nombre, precio=precio.quantize(Decimal("0.01")), stock=stock)
        if nuevo.guardar():
            for entry in (self.entry_nombre, self.entry_precio, self.entry_stock):
                entry.delete(0, tk.END)
            self.cargar_productos()
        else:
            messagebox.showerror("Error", "No se pudo guardar el producto en la base de datos.")
