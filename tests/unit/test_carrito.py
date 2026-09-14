import pytest
from src.carrito.service import CarritoService
from src.catalogo.service import CatalogoService

@pytest.fixture
def catalogo():
    cat = CatalogoService()
    # Create a mock product and variant
    prod_id = cat.crear_producto("Blusa", "Blusa roja", 50.0, 1)
    var_id = cat.agregar_variante(prod_id, stock=10)
    return cat, var_id

@pytest.fixture
def carrito(catalogo):
    cat, _ = catalogo
    return CarritoService(cat)

def test_agregar_al_carrito_exito(carrito, catalogo):
    _, var_id = catalogo

    qty = carrito.agregar_al_carrito(var_id, 2)
    assert qty == 2

    qty = carrito.agregar_al_carrito(var_id, 3)
    assert qty == 5

def test_agregar_al_carrito_sin_stock(carrito, catalogo):
    _, var_id = catalogo

    with pytest.raises(ValueError, match="Stock insuficiente"):
        carrito.agregar_al_carrito(var_id, 15)

def test_agregar_cantidad_invalida(carrito, catalogo):
    _, var_id = catalogo

    with pytest.raises(ValueError, match="mayor a cero"):
        carrito.agregar_al_carrito(var_id, 0)

    with pytest.raises(ValueError, match="mayor a cero"):
        carrito.agregar_al_carrito(var_id, -5)

def test_modificar_cantidad_carrito(carrito, catalogo):
    _, var_id = catalogo

    carrito.agregar_al_carrito(var_id, 2)
    qty = carrito.modificar_cantidad_carrito(var_id, 5)

    assert qty == 5
    assert carrito.get_items()[var_id] == 5

def test_modificar_cantidad_sin_stock(carrito, catalogo):
    _, var_id = catalogo

    carrito.agregar_al_carrito(var_id, 2)

    with pytest.raises(ValueError, match="Stock insuficiente"):
        carrito.modificar_cantidad_carrito(var_id, 15)

def test_vaciar_carrito(carrito, catalogo):
    _, var_id = catalogo

    carrito.agregar_al_carrito(var_id, 2)
    assert len(carrito.get_items()) == 1

    carrito.vaciar_carrito()
    assert len(carrito.get_items()) == 0

def test_impedir_reservar_mas_existencias(carrito, catalogo):
    cat, var_id = catalogo

    # Hay 10 en stock real inicialmente
    carrito.agregar_item(var_id, 8)
    assert cat.variantes[var_id]['stock_reservado'] == 8

    # Intentar reservar 3 más debería fallar, dado que 8 + 3 = 11 > 10
    with pytest.raises(ValueError, match="Stock insuficiente"):
        carrito.agregar_item(var_id, 3)

    assert cat.variantes[var_id]['stock_reservado'] == 8

def test_confirmar_liberacion_stock(carrito, catalogo):
    cat, var_id = catalogo

    carrito.agregar_item(var_id, 5)
    assert cat.variantes[var_id]['stock_reservado'] == 5

    # Remover 2
    carrito.remover_item(var_id, 2)
    assert cat.variantes[var_id]['stock_reservado'] == 3
    assert carrito.get_items()[var_id] == 3

    # Remover el resto
    carrito.remover_item(var_id)
    assert cat.variantes[var_id]['stock_reservado'] == 0
    assert var_id not in carrito.get_items()
