# exceptions.py
# Custom exception hierarchy for the inventory management system.
# All custom exceptions inherit from ErrorInventario, which itself
# inherits from Exception. This satisfies SRP: this file owns only
# the exception definitions.

class ErrorInventario(Exception):
    """Base class for all inventory-related errors.

    Any except block that catches ErrorInventario will also catch
    all subclasses (ProductoNoEncontrado, CantidadInvalida,
    StockInsuficiente), so the caller can decide how specific to be.
    """
    pass


class ProductoNoEncontrado(ErrorInventario):
    """Raised when a product code does not exist in the inventory."""
    pass


class CantidadInvalida(ErrorInventario):
    """Raised when the requested quantity is zero, negative, or not an integer."""
    pass


class StockInsuficiente(ErrorInventario):
    """Raised when the requested quantity exceeds the available stock."""
    pass
