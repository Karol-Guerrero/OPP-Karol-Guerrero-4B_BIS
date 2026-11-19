# inventory.py
# Defines the Inventario class. SRP: this file owns only the
# collection of products and the lookup + delegation logic.
# It does NOT validate quantity — that is Producto's responsibility.

from products import Producto
from exceptions import ProductoNoEncontrado


class Inventario:
    """A catalog of products keyed by product code."""

    def __init__(self):
        # Initial inventory — at least two additional products added
        # beyond the minimum to satisfy instruction #5.
        self.productos = {
            "P01": Producto("Laptop Lenovo IdeaPad",  stock=10),
            "P02": Producto("Mouse Inalámbrico Logitech", stock=25),
            "P03": Producto("Teclado Mecánico Redragon", stock=15),
            "P04": Producto("Monitor Samsung 24\"",    stock=8),
            "P05": Producto("Audífonos Sony WH-1000", stock=20),
        }

    def retirar(self, codigo: str, cantidad) -> int:
        """Withdraw 'cantidad' units of the product identified by 'codigo'.

        Steps:
        1. Verify the product code exists — raises ProductoNoEncontrado
           if it does not.
        2. Delegate the withdrawal to the Producto object, letting its
           exceptions (CantidadInvalida, StockInsuficiente) propagate
           naturally to the caller (instruction #7).

        Returns the remaining stock after a successful withdrawal.
        """

        # Step 1: check existence
        if codigo not in self.productos:
            raise ProductoNoEncontrado(
                f"El producto con código '{codigo}' no existe en el inventario."
            )

        # Step 2: delegate — exceptions from Producto propagate up
        producto = self.productos[codigo]
        stock_restante = producto.retirar(cantidad)
        return stock_restante

    def mostrar(self):
        """Print the current stock of all products."""
        print("\n{'─' * 40}")
        print(f"  {'CÓDIGO':<6}  {'PRODUCTO':<30}  STOCK")
        print("  " + "─" * 48)
        for codigo, producto in self.productos.items():
            print(f"  {codigo:<6}  {producto.nombre:<30}  {producto.stock}")
        print()
