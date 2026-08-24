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
            'estado': 'Pendiente',
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
