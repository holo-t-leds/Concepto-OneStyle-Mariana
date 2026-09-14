# src/carrito/service.py
from datetime import datetime, timedelta

class CarritoService:
    def __init__(self, catalogo_service):
        self.catalogo_service = catalogo_service
        self.items = {}  # variante_id: cantidad
        self.timestamps = {} # variante_id: datetime (expiracion)

    def agregar_item(self, variante_id: int, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        stock_disponible = self.catalogo_service.consultar_disponibilidad(variante_id)

        current_quantity = self.items.get(variante_id, 0)

        # Checking net availability (can only reserve up to available)
        if cantidad > stock_disponible:
            raise ValueError(f"Stock insuficiente. Solo hay {stock_disponible} unidades disponibles.")

        self.items[variante_id] = current_quantity + cantidad
        self.timestamps[variante_id] = datetime.now() + timedelta(minutes=30)

        # Increase reserved stock
        self.catalogo_service.variantes[variante_id]['stock_reservado'] += cantidad

        return self.items[variante_id]

    def agregar_al_carrito(self, variante_id: int, cantidad: int):
        # Alias para mantener compatibilidad
        return self.agregar_item(variante_id, cantidad)

    def modificar_cantidad_carrito(self, variante_id: int, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        current_quantity = self.items.get(variante_id, 0)
        difference = cantidad - current_quantity

        if difference > 0:
            stock_disponible = self.catalogo_service.consultar_disponibilidad(variante_id)
            if difference > stock_disponible:
                 raise ValueError(f"Stock insuficiente. Solo hay {stock_disponible} unidades disponibles para añadir.")
            self.catalogo_service.variantes[variante_id]['stock_reservado'] += difference
        elif difference < 0:
            self.catalogo_service.variantes[variante_id]['stock_reservado'] += difference # difference is negative

        self.items[variante_id] = cantidad
        self.timestamps[variante_id] = datetime.now() + timedelta(minutes=30)
        return self.items[variante_id]

    def remover_item(self, variante_id: int, cantidad: int = None):
        if variante_id not in self.items:
            return

        current_quantity = self.items[variante_id]
        if cantidad is None or cantidad >= current_quantity:
            # Eliminar por completo
            self.catalogo_service.variantes[variante_id]['stock_reservado'] -= current_quantity
            del self.items[variante_id]
            if variante_id in self.timestamps:
                del self.timestamps[variante_id]
        else:
            # Reducir cantidad
            self.catalogo_service.variantes[variante_id]['stock_reservado'] -= cantidad
            self.items[variante_id] -= cantidad

    def purgar_reservas_expiradas(self, tiempo_limite_minutos=30):
        now = datetime.now()
        variantes_a_remover = []
        for var_id, expires_at in self.timestamps.items():
            if now > expires_at:
                variantes_a_remover.append(var_id)

        for var_id in variantes_a_remover:
            self.remover_item(var_id)

    def vaciar_carrito(self):
        for var_id in list(self.items.keys()):
            self.remover_item(var_id)

    def get_items(self):
        return self.items.copy()
