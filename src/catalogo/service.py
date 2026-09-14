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
            'stock_real': stock,
            'stock_reservado': 0,
            'punto_reposicion': punto_reposicion
        }
        self.productos[producto_id]['variantes'].append(var_id)
        self.variante_id_counter += 1
        return var_id

    def consultar_stock_variante(self, variante_id: int) -> int:
        if variante_id not in self.variantes:
            raise ValueError("Variante no encontrada")
        return self.consultar_disponibilidad(variante_id)

    def consultar_disponibilidad(self, variante_id: int) -> int:
        if variante_id not in self.variantes:
            raise ValueError("Variante no encontrada")
        var = self.variantes[variante_id]
        return var['stock_real'] - var['stock_reservado']

    def alerta_punto_reposicion(self, variante_id: int) -> bool:
        if variante_id not in self.variantes:
            raise ValueError("Variante no encontrada")
        variante = self.variantes[variante_id]
        return self.consultar_disponibilidad(variante_id) <= variante['punto_reposicion']

    def procesar_url_imagen(self, url: str) -> str:
        """
        Valida que la URL provenga de Cloudinary CDN y la retorna.
        """
        if not url.startswith("https://res.cloudinary.com/"):
            raise ValueError("La URL de la imagen debe provenir de Cloudinary CDN.")
        return url
