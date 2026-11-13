"""
exporters.py - Lab 9

Toda la lógica de archivos (CSV, TXT, JSON y PDF) vive en este módulo.
El controlador y la vista NO importan csv, json ni fpdf: el controlador solo
instancia la clase hija elegida y llama a su método .export().

Herencia:
    Exporter  (clase base abstracta: define la "interfaz" export())
    ├── CSVExporter   -> librería nativa csv
    ├── TXTExporter   -> función nativa open()
    ├── JSONExporter  -> librería nativa json
    └── PDFExporter   -> librería de terceros fpdf

Polimorfismo:
    Las cuatro clases hijas sobrescriben export(data, file_path); quien las usa
    llama siempre a  exportador.export(productos, ruta)  sin saber qué formato es.
"""

import csv
import json
from abc import ABC, abstractmethod
from contextlib import contextmanager
from datetime import datetime

from fpdf import FPDF


class ExportError(Exception):
    """Error al exportar. Es lo único que el controlador necesita atrapar."""


# ---------------------------------------------------------------------------
# Clase base (la "interfaz")
# ---------------------------------------------------------------------------
class Exporter(ABC):
    """Contrato común: toda clase hija debe sobrescribir export()."""

    descripcion = ""      # texto para el cuadro de diálogo "Guardar como"
    extension = ""        # ".csv", ".txt", ".json", ".pdf"

    columnas = ("id", "nombre", "precio", "stock")
    encabezados = ("ID", "Nombre", "Precio", "Stock")

    @abstractmethod
    def export(self, data, file_path):
        """Método que debe ser sobrescrito por las clases hijas.

        data:      lista de productos (diccionarios o tuplas id, nombre, precio, stock).
        file_path: ruta donde se guardará el archivo.
        Devuelve la ruta final del archivo generado.
        """
        raise NotImplementedError("Este método debe ser implementado por la subclase.")

    # --- utilidades compartidas por las clases hijas -------------------------
    def _normalizar(self, data):
        """Convierte lo que devuelve la base de datos en filas simples."""
        filas = []

        for producto in data:
            if isinstance(producto, dict):
                valores = [producto[columna] for columna in self.columnas]
            else:
                valores = list(producto)[:4]

            filas.append({
                "id": int(valores[0]),
                "nombre": str(valores[1]),
                "precio": round(float(valores[2]), 2),   # Decimal -> float
                "stock": int(valores[3]),
            })

        return filas

    def _preparar_ruta(self, file_path):
        """Agrega la extensión si el usuario no la escribió."""
        file_path = str(file_path)

        if not file_path.lower().endswith(self.extension):
            file_path += self.extension

        return file_path

    @contextmanager
    def _proteger(self):
        """Convierte cualquier fallo de archivo en un ExportError."""
        try:
            yield
        except ExportError:
            raise
        except Exception as error:
            raise ExportError(f"No se pudo guardar el archivo: {error}") from error

    @staticmethod
    def _fecha():
        return datetime.now().strftime("%d/%m/%Y %H:%M")


# ---------------------------------------------------------------------------
# Clases hijas
# ---------------------------------------------------------------------------
class CSVExporter(Exporter):
    descripcion = "Archivo CSV"
    extension = ".csv"

    def export(self, data, file_path):
        with self._proteger():
            filas = self._normalizar(data)
            file_path = self._preparar_ruta(file_path)

            # utf-8-sig: Excel muestra bien los acentos. newline="": lo requiere csv.
            with open(file_path, "w", encoding="utf-8-sig", newline="") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(self.columnas)

                for fila in filas:
                    escritor.writerow([
                        fila["id"],
                        fila["nombre"],
                        f"{fila['precio']:.2f}",
                        fila["stock"],
                    ])

        return file_path


class TXTExporter(Exporter):
    descripcion = "Archivo de texto"
    extension = ".txt"

    def export(self, data, file_path):
        with self._proteger():
            filas = self._normalizar(data)
            file_path = self._preparar_ruta(file_path)

            ancho = max([len(self.encabezados[1])] + [len(f["nombre"]) for f in filas])
            linea = "-" * (5 + 2 + ancho + 2 + 12 + 2 + 7)

            with open(file_path, "w", encoding="utf-8") as archivo:
                archivo.write("--- REPORTE DE PRODUCTOS ---\n")
                archivo.write(f"Generado: {self._fecha()}\n")
                archivo.write(linea + "\n")
                archivo.write(f"{'ID':>5}  {'Nombre':<{ancho}}  {'Precio':>12}  {'Stock':>7}\n")
                archivo.write(linea + "\n")

                for fila in filas:
                    archivo.write(
                        f"{fila['id']:>5}  {fila['nombre']:<{ancho}}  "
                        f"{fila['precio']:>12.2f}  {fila['stock']:>7}\n"
                    )

                archivo.write(linea + "\n")
                archivo.write(f"Total de productos: {len(filas)}\n")

        return file_path


class JSONExporter(Exporter):
    descripcion = "Archivo JSON"
    extension = ".json"

    def export(self, data, file_path):
        with self._proteger():
            filas = self._normalizar(data)
            file_path = self._preparar_ruta(file_path)

            with open(file_path, "w", encoding="utf-8") as archivo:
                json.dump(filas, archivo, ensure_ascii=False, indent=4)
                archivo.write("\n")

        return file_path


# --- PDF --------------------------------------------------------------------
def _latin1(texto):
    """Las fuentes básicas de fpdf usan latin-1 (acentos y ñ funcionan);
    lo que no exista en latin-1 se cambia por '?' en lugar de truncar el PDF."""
    return str(texto).encode("latin-1", "replace").decode("latin-1")


class _ReportePDF(FPDF):
    """Documento PDF con título y encabezado de tabla en cada página."""

    anchos = (20, 90, 40, 30)

    def __init__(self, encabezados, fecha):
        super().__init__()
        self.encabezados = encabezados
        self.fecha = fecha

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Reporte de Inventario de Productos", 0, 1, "C")
        self.set_font("Arial", "", 9)
        self.cell(0, 6, f"Generado: {self.fecha}", 0, 1, "C")
        self.ln(4)

        # Encabezado de la tabla (se repite en cada página).
        self.set_font("Arial", "B", 11)
        self.set_fill_color(20, 33, 61)
        self.set_text_color(255, 255, 255)

        for ancho, titulo, alineacion in zip(self.anchos, self.encabezados, ("C", "L", "R", "R")):
            self.cell(ancho, 9, _latin1(titulo), 1, 0, alineacion, True)

        self.ln(9)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", 0, 0, "C")


class PDFExporter(Exporter):
    descripcion = "Documento PDF"
    extension = ".pdf"

    def export(self, data, file_path):
        with self._proteger():
            filas = self._normalizar(data)
            file_path = self._preparar_ruta(file_path)

            pdf = _ReportePDF(self.encabezados, self._fecha())
            pdf.alias_nb_pages()
            pdf.set_margins(15, 15, 15)
            pdf.set_title("Reporte de Inventario de Productos")
            pdf.add_page()

            pdf.set_font("Arial", "", 10)
            a_id, a_nombre, a_precio, a_stock = pdf.anchos

            for numero, fila in enumerate(filas):
                relleno = numero % 2 == 1                   # filas alternadas
                pdf.set_fill_color(235, 239, 247)

                pdf.cell(a_id, 8, str(fila["id"]), 1, 0, "C", relleno)
                pdf.cell(a_nombre, 8, _latin1(fila["nombre"]), 1, 0, "L", relleno)
                pdf.cell(a_precio, 8, f"{fila['precio']:.2f}", 1, 0, "R", relleno)
                pdf.cell(a_stock, 8, str(fila["stock"]), 1, 1, "R", relleno)

            pdf.ln(4)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 8, f"Total de productos: {len(filas)}", 0, 1, "L")

            pdf.output(file_path)

        return file_path


# ---------------------------------------------------------------------------
# Formatos disponibles: nombre que ve el usuario -> clase hija
# ---------------------------------------------------------------------------
EXPORTERS = {
    "CSV": CSVExporter,
    "TXT": TXTExporter,
    "JSON": JSONExporter,
    "PDF": PDFExporter,
}
