# src/catalogo/service.py

class CatalogoService:
    def __init__(self):
        # In memory storage for demo
        self.productos = {}
        self.variantes = {} # variante_id: {'producto_id': int, 'stock': int, 'punto_reposicion': int}
        self.producto_id_counter = 1
        self.variante_id_counter = 1

    def crear_producto(self, nombre: str, descripcion: str, precio: float, categoria_id: int):
        prod_id = self.producto_id_counter
        self.productos[prod_id] = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'categoria_id': categoria_id,
            'variantes': []
        }
        self.producto_id_counter += 1
        return prod_id

    def agregar_variante(self, producto_id: int, stock: int, punto_reposicion: int = 5):
        if producto_id not in self.productos:
            raise ValueError("Producto no encontrado")

        var_id = self.variante_id_counter
        self.variantes[var_id] = {
            'producto_id': producto_id,
            'stock': stock,
            'punto_reposicion': punto_reposicion
        }
        self.productos[producto_id]['variantes'].append(var_id)
        self.variante_id_counter += 1
        return var_id

    def consultar_stock_variante(self, variante_id: int) -> int:
        if variante_id not in self.variantes:
            raise ValueError("Variante no encontrada")
        return self.variantes[variante_id]['stock']

    def alerta_punto_reposicion(self, variante_id: int) -> bool:
        if variante_id not in self.variantes:
            raise ValueError("Variante no encontrada")
        variante = self.variantes[variante_id]
        return variante['stock'] <= variante['punto_reposicion']
