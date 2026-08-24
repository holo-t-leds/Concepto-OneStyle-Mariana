import pytest
import urllib.parse
from src.pedidos.service import PedidosService
from src.catalogo.service import CatalogoService

@pytest.fixture
def catalogo():
    cat = CatalogoService()
    # Create products and variants
    prod_id1 = cat.crear_producto("Blusa", "Blusa roja", 50.0, 1)
    var_id1 = cat.agregar_variante(prod_id1, stock=10)

    prod_id2 = cat.crear_producto("Pantalón", "Jean azul", 80.0, 2)
    var_id2 = cat.agregar_variante(prod_id2, stock=5)

    return cat, var_id1, var_id2

@pytest.fixture
def pedidos(catalogo):
    cat, _, _ = catalogo
    return PedidosService(cat)

def test_crear_pedido(pedidos, catalogo):
    _, var_id1, var_id2 = catalogo

    items = {
        var_id1: 2, # 2 * 50 = 100
        var_id2: 1  # 1 * 80 = 80
    }

    pedido_id = pedidos.crear_pedido(usuario_id=1, items_carrito=items)

    assert pedido_id == 1
    pedido = pedidos.pedidos[pedido_id]
    assert pedido['usuario_id'] == 1
    assert pedido['total'] == 180.0
    assert pedido['estado'] == 'Pendiente'

def test_crear_pedido_vacio(pedidos):
    with pytest.raises(ValueError, match="El carrito está vacío."):
        pedidos.crear_pedido(usuario_id=1, items_carrito={})

def test_calcular_total(pedidos, catalogo):
    _, var_id1, var_id2 = catalogo

    items = {
        var_id1: 3, # 3 * 50 = 150
        var_id2: 2  # 2 * 80 = 160
    }

    total = pedidos.calcular_total(items)
    assert total == 310.0

def test_generar_enlace_whatsapp(pedidos, catalogo):
    _, var_id1, _ = catalogo

    items = {var_id1: 1} # total = 50.0
    pedido_id = pedidos.crear_pedido(usuario_id=1, items_carrito=items)

    enlace = pedidos.generar_enlace_whatsapp(pedido_id, "573001234567")

    mensaje_esperado = f"Hola, me gustaría confirmar el pedido #{pedido_id}. El total es $50.00."
    mensaje_codificado = urllib.parse.quote(mensaje_esperado)

    assert enlace == f"https://wa.me/573001234567?text={mensaje_codificado}"

def test_calcular_total_vacio(pedidos):
    total = pedidos.calcular_total({})
    assert total == 0.0
