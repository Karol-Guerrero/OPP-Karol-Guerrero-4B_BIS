"""
app_movil.py - Lab 10

Lógica de perfiles de una aplicación móvil con programación orientada a objetos:
herencia (PerfilPro extiende PerfilMovil), encapsulamiento de reglas de negocio
y excepciones propias para los estados anómalos.
"""


# ---------------------------------------------------------------------------
# Jerarquía de excepciones del dominio
# ---------------------------------------------------------------------------
class SuscripcionExpiradaError(Exception):
    """Se intentó una operación restringida sin una membresía activa."""


class PuntosInsuficientesError(Exception):
    """La transacción supera el saldo de gemas disponible."""


# ---------------------------------------------------------------------------
# Clase base
# ---------------------------------------------------------------------------
class PerfilMovil:
    """Perfil básico de un usuario de la app."""

    def __init__(self, username, gemas=50, racha_dias=1, notificaciones_activas=True):
        # Validación estricta: las gemas deben ser un entero no negativo.
        if not self._es_entero(gemas) or gemas < 0:
            raise ValueError("Las gemas iniciales deben ser un entero no negativo.")

        self.username = username
        self.gemas = gemas
        self.racha_dias = racha_dias
        self.notificaciones_activas = notificaciones_activas

    @staticmethod
    def _es_entero(valor):
        """True solo para enteros reales (bool es subclase de int, pero no cuenta)."""
        return isinstance(valor, int) and not isinstance(valor, bool)

    def _validar_cantidad(self, cantidad):
        """La cantidad debe ser un entero estrictamente positivo."""
        if not self._es_entero(cantidad) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")

    def ganar_gemas(self, cantidad: int) -> int:
        """Suma gemas al saldo y devuelve el saldo actualizado."""
        self._validar_cantidad(cantidad)
        self.gemas += cantidad
        return self.gemas

    def gastar_gemas(self, cantidad: int) -> int:
        """Resta gemas del saldo (si alcanza) y devuelve el saldo actualizado."""
        self._validar_cantidad(cantidad)

        if cantidad > self.gemas:
            raise PuntosInsuficientesError(
                f"Gemas insuficientes: tienes {self.gemas} y necesitas {cantidad}."
            )

        self.gemas -= cantidad
        return self.gemas


# ---------------------------------------------------------------------------
# Subclase derivada
# ---------------------------------------------------------------------------
class PerfilPro(PerfilMovil):
    """Perfil con suscripción Pro: hereda todo y agrega contenido offline."""

    def __init__(self, username, meses_suscripcion, gemas=50, racha_dias=1,
                 notificaciones_activas=True):
        super().__init__(username, gemas, racha_dias, notificaciones_activas)

        if not self._es_entero(meses_suscripcion) or meses_suscripcion <= 0:
            raise ValueError("El periodo inicial de suscripción debe ser mayor a cero.")

        self.meses_suscripcion = meses_suscripcion
        self.es_pro = True

    def descargar_contenido_offline(self) -> str:
        """Confirma la descarga si la suscripción sigue vigente.

        Si los meses llegaron a 0 (o la membresía ya estaba desactivada),
        pasa es_pro a False y propaga SuscripcionExpiradaError.
        """
        if self.meses_suscripcion <= 0 or not self.es_pro:
            self.es_pro = False
            raise SuscripcionExpiradaError(
                f"La suscripción de {self.username} expiró: no puede descargar contenido offline."
            )

        return f"Contenido offline descargado correctamente para {self.username}."
