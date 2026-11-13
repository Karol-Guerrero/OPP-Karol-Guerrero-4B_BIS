"""
test_app_movil.py - Lab 10

Suite de pruebas unitarias con pytest para app_movil.py.
Ejecutar:  pytest -v
"""

import pytest

from app_movil import (
    PerfilMovil,
    PerfilPro,
    PuntosInsuficientesError,
    SuscripcionExpiradaError,
)


# ---------------------------------------------------------------------------
# Fixtures: instancias nuevas para cada prueba (aislamiento de estado)
# ---------------------------------------------------------------------------
@pytest.fixture
def perfil():
    """PerfilMovil estándar: 50 gemas, racha de 1 día."""
    return PerfilMovil("karol")


@pytest.fixture
def perfil_pro():
    """PerfilPro con 3 meses de suscripción."""
    return PerfilPro("karol_pro", meses_suscripcion=3)


# ---------------------------------------------------------------------------
# Integridad estructural: valores iniciales
# ---------------------------------------------------------------------------
def test_atributos_iniciales_por_defecto(perfil):
    assert perfil.username == "karol"
    assert perfil.gemas == 50
    assert perfil.racha_dias == 1
    assert perfil.notificaciones_activas is True


def test_atributos_iniciales_personalizados():
    p = PerfilMovil("ana", gemas=120, racha_dias=7, notificaciones_activas=False)
    assert (p.gemas, p.racha_dias, p.notificaciones_activas) == (120, 7, False)


def test_gemas_iniciales_en_cero_son_validas():
    assert PerfilMovil("ana", gemas=0).gemas == 0


def test_fixture_aisla_el_estado_entre_pruebas(perfil):
    # Si el estado se compartiera entre pruebas, otras pruebas que gastan
    # o ganan gemas harían fallar esta comprobación.
    perfil.ganar_gemas(1000)
    assert perfil.gemas == 1050


def test_fixture_entrega_estado_limpio(perfil):
    assert perfil.gemas == 50


# ---------------------------------------------------------------------------
# Consistencia aritmética de las transacciones
# ---------------------------------------------------------------------------
def test_ganar_gemas_suma_y_devuelve_el_nuevo_saldo(perfil):
    assert perfil.ganar_gemas(20) == 70
    assert perfil.gemas == 70


def test_gastar_gemas_resta_y_devuelve_el_nuevo_saldo(perfil):
    assert perfil.gastar_gemas(30) == 20
    assert perfil.gemas == 20


def test_ganar_y_gastar_son_consistentes(perfil):
    perfil.ganar_gemas(25)
    perfil.gastar_gemas(25)
    assert perfil.gemas == 50


def test_gastar_todo_el_saldo_deja_cero(perfil):
    assert perfil.gastar_gemas(50) == 0


# ---------------------------------------------------------------------------
# Validación de excepciones con pytest.raises
# ---------------------------------------------------------------------------
def test_gemas_iniciales_negativas_lanzan_value_error():
    with pytest.raises(ValueError):
        PerfilMovil("ana", gemas=-1)


def test_gastar_mas_de_lo_disponible_lanza_puntos_insuficientes(perfil):
    with pytest.raises(PuntosInsuficientesError, match="insuficientes"):
        perfil.gastar_gemas(51)


def test_gasto_rechazado_no_modifica_el_saldo(perfil):
    with pytest.raises(PuntosInsuficientesError):
        perfil.gastar_gemas(500)
    assert perfil.gemas == 50


def test_ganar_gemas_invalidas_no_modifica_el_saldo(perfil):
    with pytest.raises(ValueError):
        perfil.ganar_gemas(-10)
    assert perfil.gemas == 50


def test_perfil_pro_con_cero_meses_lanza_value_error():
    with pytest.raises(ValueError):
        PerfilPro("ana", meses_suscripcion=0)


def test_perfil_pro_con_meses_negativos_lanza_value_error():
    with pytest.raises(ValueError):
        PerfilPro("ana", meses_suscripcion=-2)


def test_descarga_con_suscripcion_expirada_lanza_error(perfil_pro):
    perfil_pro.meses_suscripcion = 0
    with pytest.raises(SuscripcionExpiradaError, match="expiró"):
        perfil_pro.descargar_contenido_offline()


def test_descarga_expirada_desactiva_es_pro(perfil_pro):
    perfil_pro.meses_suscripcion = 0
    with pytest.raises(SuscripcionExpiradaError):
        perfil_pro.descargar_contenido_offline()
    assert perfil_pro.es_pro is False


# ---------------------------------------------------------------------------
# Pruebas parametrizadas: valores límite al ganar y gastar gemas
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "cantidad, saldo_esperado",
    [
        (1, 51),          # límite inferior válido
        (10, 60),
        (50, 100),
        (1000, 1050),
        (10**9, 10**9 + 50),
    ],
)
def test_ganar_gemas_cantidades_validas(perfil, cantidad, saldo_esperado):
    assert perfil.ganar_gemas(cantidad) == saldo_esperado


@pytest.mark.parametrize(
    "cantidad_invalida",
    [0, -1, -100, 2.5, "10", None, True],
)
def test_ganar_gemas_cantidades_invalidas(perfil, cantidad_invalida):
    with pytest.raises(ValueError):
        perfil.ganar_gemas(cantidad_invalida)


@pytest.mark.parametrize(
    "cantidad, saldo_esperado",
    [
        (1, 49),          # límite inferior válido
        (25, 25),
        (49, 1),
        (50, 0),          # límite superior válido: gasta todo el saldo
    ],
)
def test_gastar_gemas_cantidades_validas(perfil, cantidad, saldo_esperado):
    assert perfil.gastar_gemas(cantidad) == saldo_esperado


@pytest.mark.parametrize("cantidad_invalida", [0, -5, 1.5, "3", None])
def test_gastar_gemas_cantidades_invalidas(perfil, cantidad_invalida):
    with pytest.raises(ValueError):
        perfil.gastar_gemas(cantidad_invalida)


@pytest.mark.parametrize("cantidad", [51, 100, 10**6])
def test_gastar_gemas_por_encima_del_saldo(perfil, cantidad):
    with pytest.raises(PuntosInsuficientesError):
        perfil.gastar_gemas(cantidad)


# ---------------------------------------------------------------------------
# Tipo y jerarquía: isinstance / herencia y ciclo de vida de PerfilPro
# ---------------------------------------------------------------------------
def test_perfil_pro_es_instancia_de_perfil_movil(perfil_pro):
    assert isinstance(perfil_pro, PerfilPro)
    assert isinstance(perfil_pro, PerfilMovil)
    assert issubclass(PerfilPro, PerfilMovil)


def test_perfil_movil_no_es_perfil_pro(perfil):
    assert isinstance(perfil, PerfilMovil)
    assert not isinstance(perfil, PerfilPro)


def test_perfil_pro_hereda_los_valores_por_defecto(perfil_pro):
    assert perfil_pro.gemas == 50
    assert perfil_pro.racha_dias == 1
    assert perfil_pro.notificaciones_activas is True


def test_perfil_pro_agrega_atributos_propios(perfil_pro):
    assert perfil_pro.meses_suscripcion == 3
    assert perfil_pro.es_pro is True


def test_perfil_pro_hereda_los_metodos_de_gemas(perfil_pro):
    assert perfil_pro.ganar_gemas(10) == 60
    assert perfil_pro.gastar_gemas(60) == 0
    with pytest.raises(PuntosInsuficientesError):
        perfil_pro.gastar_gemas(1)


def test_excepciones_de_dominio_heredan_de_exception():
    assert issubclass(SuscripcionExpiradaError, Exception)
    assert issubclass(PuntosInsuficientesError, Exception)
    assert not issubclass(SuscripcionExpiradaError, PuntosInsuficientesError)


def test_ciclo_de_vida_de_la_suscripcion_pro(perfil_pro):
    # 1) Suscripción vigente: la descarga funciona.
    resultado = perfil_pro.descargar_contenido_offline()
    assert isinstance(resultado, str)
    assert "correctamente" in resultado
    assert perfil_pro.es_pro is True

    # 2) La suscripción vence: se lanza el error y se pierde el estado Pro.
    perfil_pro.meses_suscripcion = 0
    with pytest.raises(SuscripcionExpiradaError):
        perfil_pro.descargar_contenido_offline()
    assert perfil_pro.es_pro is False

    # 3) Sigue sin poder descargar mientras no se renueve.
    with pytest.raises(SuscripcionExpiradaError):
        perfil_pro.descargar_contenido_offline()
