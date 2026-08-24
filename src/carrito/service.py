# src/carrito/service.py

class CarritoService:
    def __init__(self, catalogo_service):
        self.catalogo_service = catalogo_service
        self.items = {}  # variante_id: cantidad

    def agregar_al_carrito(self, variante_id: int, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        stock_disponible = self.catalogo_service.consultar_stock_variante(variante_id)

        current_quantity = self.items.get(variante_id, 0)
        if current_quantity + cantidad > stock_disponible:
            raise ValueError(f"Stock insuficiente. Solo hay {stock_disponible} unidades disponibles.")

        self.items[variante_id] = current_quantity + cantidad
        return self.items[variante_id]

    def modificar_cantidad_carrito(self, variante_id: int, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        stock_disponible = self.catalogo_service.consultar_stock_variante(variante_id)

        if cantidad > stock_disponible:
             raise ValueError(f"Stock insuficiente. Solo hay {stock_disponible} unidades disponibles.")

        self.items[variante_id] = cantidad
        return self.items[variante_id]

    def vaciar_carrito(self):
        self.items.clear()

    def get_items(self):
        return self.items.copy()
