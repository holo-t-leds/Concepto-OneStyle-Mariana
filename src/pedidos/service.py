# src/pedidos/service.py
import urllib.parse
from datetime import datetime

class PedidosService:
    def __init__(self, catalogo_service):
        self.catalogo_service = catalogo_service
        self.pedidos = {}
        self.pedido_id_counter = 1

    def crear_pedido(self, usuario_id: int, items_carrito: dict):
        if not items_carrito:
            raise ValueError("El carrito está vacío.")

        total = self.calcular_total(items_carrito)

        pedido_id = self.pedido_id_counter
        self.pedidos[pedido_id] = {
            'usuario_id': usuario_id,
            'items': items_carrito.copy(),
            'total': total,
            'estado': 'Registrado',
            'fecha': datetime.now()
        }
        self.pedido_id_counter += 1

        return pedido_id

    def calcular_total(self, items_carrito: dict) -> float:
        total = 0.0
        for variante_id, cantidad in items_carrito.items():
            variante = self.catalogo_service.variantes.get(variante_id)
            if not variante:
                raise ValueError(f"Variante {variante_id} no encontrada.")
            producto_id = variante['producto_id']
            producto = self.catalogo_service.productos.get(producto_id)
            if not producto:
                 raise ValueError(f"Producto {producto_id} no encontrado.")

            total += producto['precio'] * cantidad

        return total

    def generar_enlace_whatsapp(self, pedido_id: int, telefono_vendedora: str) -> str:
        if pedido_id not in self.pedidos:
            raise ValueError("Pedido no encontrado.")

        pedido = self.pedidos[pedido_id]
        mensaje = f"Hola, me gustaría confirmar el pedido #{pedido_id}. El total es ${pedido['total']:.2f}."

        mensaje_codificado = urllib.parse.quote(mensaje)

        # Asumiendo un número internacional sin +, por ej: 573001234567
        return f"https://wa.me/{telefono_vendedora}?text={mensaje_codificado}"

    def transicionar_estado(self, pedido_id: int, nuevo_estado: str):
        if pedido_id not in self.pedidos:
            raise ValueError("Pedido no encontrado.")

        pedido = self.pedidos[pedido_id]
        estado_actual = pedido['estado']

        estados_validos = ['Registrado', 'Confirmado', 'En Empaque', 'Despachado', 'Entregado', 'Cancelado']
        if nuevo_estado not in estados_validos:
            raise ValueError(f"Estado '{nuevo_estado}' no es válido.")

        if estado_actual == nuevo_estado:
            return

        # Máquina de estados
        if nuevo_estado == 'Cancelado':
            if estado_actual not in ['Registrado', 'Confirmado']:
                raise ValueError("Solo se puede cancelar desde Registrado o Confirmado.")
        elif estado_actual == 'Registrado' and nuevo_estado != 'Confirmado':
            raise ValueError(f"Transición inválida de Registrado a {nuevo_estado}.")
        elif estado_actual == 'Confirmado' and nuevo_estado != 'En Empaque':
            raise ValueError(f"Transición inválida de Confirmado a {nuevo_estado}.")
        elif estado_actual == 'En Empaque' and nuevo_estado != 'Despachado':
            raise ValueError(f"Transición inválida de En Empaque a {nuevo_estado}.")
        elif estado_actual == 'Despachado' and nuevo_estado != 'Entregado':
            raise ValueError(f"Transición inválida de Despachado a {nuevo_estado}.")
        elif estado_actual in ['Entregado', 'Cancelado']:
            raise ValueError("El pedido está en un estado final y no puede transicionar.")

        # Acciones en transiciones
        if nuevo_estado == 'Confirmado':
            # Al pasar a Confirmado, se descuenta definitivamente stock_real y se descuenta stock_reservado
            for var_id, cantidad in pedido['items'].items():
                self.catalogo_service.variantes[var_id]['stock_real'] -= cantidad
                self.catalogo_service.variantes[var_id]['stock_reservado'] -= cantidad

        if nuevo_estado == 'Cancelado':
            # Si transiciona a Cancelado, se libera el stock reservado (o se reingresa si ya fue confirmado)
            if estado_actual == 'Registrado':
                # Todavía estaba solo reservado
                for var_id, cantidad in pedido['items'].items():
                    self.catalogo_service.variantes[var_id]['stock_reservado'] -= cantidad
            elif estado_actual == 'Confirmado':
                # Ya se había descontado real y reservado, hay que reingresarlo al real
                for var_id, cantidad in pedido['items'].items():
                    self.catalogo_service.variantes[var_id]['stock_real'] += cantidad

        pedido['estado'] = nuevo_estado
