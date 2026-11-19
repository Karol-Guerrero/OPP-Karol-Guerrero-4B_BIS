# main.py
# Entry point for the inventory management system.
# SRP: this file owns only the user interaction (menu, I/O, error display).
# All business logic lives in products.py, inventory.py, and exceptions.py.

from inventory import Inventario
from exceptions import ErrorInventario  # catches all custom subclasses


def main():
    inventario = Inventario()

    print("=" * 52)
    print("   SISTEMA DE GESTIÓN DE INVENTARIO")
    print("=" * 52)

    while True:
        # Show current stock before each operation
        inventario.mostrar()

        print("Opciones:")
        print("  [1] Retirar producto")
        print("  [2] Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "2":
            print("¡Hasta luego!")
            break

        if opcion != "1":
            print("Opción no válida. Intenta de nuevo.\n")
            continue

        # --- Gather inputs ---
        codigo = input("Código del producto: ").strip().upper()

        # try/except for ValueError: user enters text instead of a number
        try:
            cantidad = int(input("Cantidad a retirar: "))

        except ValueError:
            # Test 6: text instead of a number
            print("❌ Error: la cantidad debe ser un número entero.\n")
            continue

        # try/except/else for inventory operations
        try:
            stock_restante = inventario.retirar(codigo, cantidad)

        except ErrorInventario as e:
            # Catches ProductoNoEncontrado (Test 2),
            #         CantidadInvalida   (Tests 3, 4),
            #         StockInsuficiente  (Test 5)
            print(f"❌ Error de inventario: {e}\n")

        else:
            # else runs ONLY when no exception was raised (Test 1)
            print(f"✅ Retiro exitoso. Stock restante de '{codigo}': {stock_restante} unidades.\n")


# Entry point
if __name__ == "__main__":
    main()
