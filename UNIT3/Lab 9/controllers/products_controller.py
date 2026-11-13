from decimal import Decimal, InvalidOperation

from exporters import EXPORTERS, ExportError
from models.products_model import Producto


class ProductsController:
    """Conecta la pantalla de productos con el modelo y con los exportadores.

    Regla del Lab 9: aquí NO se importa csv, json ni fpdf. Para exportar solo se
    instancia la clase hija del formato elegido y se llama a su método .export().
    """

    def __init__(self, modelo, vista, al_cerrar_sesion=None, al_salir=None):
        self.modelo = modelo
        self.vista = vista

        self.vista.btn_guardar.config(command=self.guardar_producto)

        # El botón "Exportar Reporte" manda al controlador el formato del Combobox.
        self.vista.btn_exportar.config(
            command=lambda: self.generar_reporte(self.vista.obtener_formato())
        )

        if al_cerrar_sesion is not None:
            self.vista.btn_cerrar_sesion.config(command=al_cerrar_sesion)

        if al_salir is not None:
            self.vista.ventana.protocol("WM_DELETE_WINDOW", al_salir)

        self.cargar_productos()

    def cargar_productos(self):
        productos = self.modelo.obtener_todos()

        if productos is None:
            self.vista.mostrar_mensaje(
                "Error de conexión",
                "No se pudieron cargar los productos de la base de datos.",
                "error"
            )
            return

        self.vista.cargar_tabla(productos)

    def guardar_producto(self):
        nombre, precio_txt, stock_txt = self.vista.obtener_datos_formulario()
        precio_txt = precio_txt.replace(",", ".")

        if not nombre or not precio_txt or not stock_txt:
            self.vista.mostrar_mensaje(
                "Campos vacíos", "Completa nombre, precio y stock.", "warning"
            )
            return

        try:
            precio = Decimal(precio_txt)
            stock = int(stock_txt)
        except (InvalidOperation, ValueError):
            self.vista.mostrar_mensaje(
                "Datos inválidos",
                "El precio debe ser un número (ej. 350.00) y el stock un número entero.",
                "warning"
            )
            return

        if not precio.is_finite() or precio < 0 or stock < 0:
            self.vista.mostrar_mensaje(
                "Datos inválidos", "El precio y el stock no pueden ser negativos.", "warning"
            )
            return

        nuevo = Producto(
            nombre=nombre, precio=precio.quantize(Decimal("0.01")), stock=stock
        )

        if nuevo.guardar():
            self.vista.limpiar_formulario()
            self.cargar_productos()
        else:
            self.vista.mostrar_mensaje(
                "Error", "No se pudo guardar el producto en la base de datos.", "error"
            )

    def generar_reporte(self, formato):
        """Exporta los productos al formato elegido en la vista (polimorfismo)."""
        clase_exportador = EXPORTERS.get(formato)

        if clase_exportador is None:
            self.vista.mostrar_mensaje(
                "Formato no válido", f"Formato no soportado: {formato}", "error"
            )
            return

        productos = self.modelo.obtener_todos()

        if productos is None:
            self.vista.mostrar_mensaje(
                "Error de conexión",
                "No se pudieron leer los productos de la base de datos.",
                "error"
            )
            return

        if not productos:
            self.vista.mostrar_mensaje(
                "Sin datos", "No hay productos para exportar.", "warning"
            )
            return

        exportador = clase_exportador()      # solo se instancia la clase elegida

        ruta = self.vista.pedir_ruta_guardado(exportador.extension, exportador.descripcion)

        if not ruta:        # el usuario canceló el cuadro de diálogo
            return

        try:
            # Una sola llamada para todos los formatos: no importa cuál sea.
            ruta_final = exportador.export(productos, ruta)
        except ExportError as error:
            self.vista.mostrar_mensaje("Error al exportar", str(error), "error")
            return

        self.vista.mostrar_mensaje(
            "Exportación exitosa",
            f"Se exportaron {len(productos)} productos a:\n{ruta_final}"
        )
