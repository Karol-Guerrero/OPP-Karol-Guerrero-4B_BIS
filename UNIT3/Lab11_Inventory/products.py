# products.py
# Defines the Producto class. SRP: this file owns only the
# product data and its withdrawal validation logic.

from exceptions import CantidadInvalida, StockInsuficiente


class Producto:
    """Represents a single product with a name and available stock."""

    def __init__(self, nombre: str, stock: int):
        self.nombre = nombre
        self.stock = stock

    def retirar(self, cantidad) -> int:
        """Withdraw 'cantidad' units from stock.

        Validations (in order):
        1. cantidad must be a positive integer — raises CantidadInvalida
           if it is zero, negative, or not an integer type.
        2. cantidad must not exceed the current stock — raises
           StockInsuficiente if the request cannot be fulfilled.

        Returns the remaining stock after a successful withdrawal.
        """

        # Validation 1: type check — accept only int values
        # (bool is a subclass of int in Python, so we exclude it explicitly)
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise CantidadInvalida(
                f"La cantidad debe ser un entero, no '{type(cantidad).__name__}'."
            )

        # Validation 2: value must be strictly positive
        if cantidad <= 0:
            raise CantidadInvalida(
                f"La cantidad debe ser mayor que cero. Se recibió: {cantidad}."
            )

        # Validation 3: enough stock available
        if cantidad > self.stock:
            raise StockInsuficiente(
                f"Stock insuficiente para '{self.nombre}'. "
                f"Disponible: {self.stock}, solicitado: {cantidad}."
            )

        # All validations passed — deduct and return remaining stock
        self.stock -= cantidad
        return self.stock

    def __repr__(self):
        return f"Producto(nombre={self.nombre!r}, stock={self.stock})"
