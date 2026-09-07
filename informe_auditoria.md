# Informe de Auditoría Técnica y Aseguramiento de Calidad (QA)

## 1. Auditoría de Base de Datos, DDL y Diccionario

**Veredicto:** Aprobado con observaciones menores resueltas.

*   **Cantidad de Tablas:** Se confirmó la existencia de exactamente 20 tablas físicas en el script DDL `database/schema.sql` y en el diccionario de datos (`docs/diccionariodatos.md`).
*   **Campo de Precio:** Se verificó que la tabla `producto` contiene correctamente el campo `precio_detallista`, cumpliendo con el modelo B2C unitario.
*   **Existencia de Tablas Clave:**
    *   La tabla de trazabilidad se denomina correctamente `auditoria` (no `logs_auditoria`).
    *   Existe la tabla independiente `domicilio`, la cual está correctamente vinculada a la tabla `pedido`.
    *   La tabla `detalle_carrito` incluye los campos `cantidad_reservada` y `fecha_expiracion` para el manejo de inventario temporal.
*   **Diccionario de Datos:** Se contrastó el DDL frente al diccionario y se verificó que la estructura coincide. Se corrigió el nombre comercial en el título del diccionario de datos para estandarizarlo a "G.C.L.".

## 2. Trazabilidad Bidireccional con la Matriz de Requisitos

**Veredicto:** Aprobado.

*   Los requisitos funcionales críticos (RF-001 a RF-013, RF-CART-010, RF-ORD-001) tienen correspondencia directa con los Casos de Uso.
*   Existe alineación directa entre las reglas de negocio y las tablas del DDL:
    *   El **borrado lógico** se soporta correctamente mediante los campos booleanos `estado_visibilidad` en `producto` y `estado_usuario` en `usuarios`, en lugar de un `DELETE` físico.
    *   El **descuento de existencias a nivel de variante** es consistente con la relación entre `detalle_pedido`, `producto_atributo` e `inventario`, manejando correctamente el `stock_disponible`.

## 3. Coherencia de Casos de Uso, Modularidad e Historias de Usuario (HU)

**Veredicto:** Aprobado.

*   **Modularidad:** Los diagramas PlantUML (`.puml`) y sus imágenes renderizadas respetan la división estricta en 5 módulos funcionales, con los actores asignados adecuadamente (Clienta, Vendedora, Administradora):
    1.  Módulo 1: Seguridad y Usuarios
    2.  Módulo 2: Catálogo e Inventario
    3.  Módulo 3: Carrito de Compras
    4.  Módulo 4: Pedidos y Gestión OMS
    5.  Módulo 5: Soporte y FAQ
*   **Historias de Usuario y Reglas:** Se validó la lógica de selección de variantes obligatoria (talla/color), control de reservas, y la redirección y estructuración al canal de WhatsApp, formalizado en las tablas `pedido`, `domicilio` y `detalle_pedido`.

## 4. Integridad de Enlaces y Recursos en README.md

**Veredicto:** Aprobado con reparaciones.

*   **Rutas de Imágenes:** Se corrigió el uso de caracteres especiales y codificación URL (como `%20`) en los enlaces del `README.md` hacia los mockups (`catalogo (2).png`, `Detalle prenda (1).png`, `404(1).png`). Los enlaces operan correctamente usando la sintaxis de markdown `<ruta>` para nombres con espacios.
*   **Unificación de Marca:** Se unificó la denominación comercial en la documentación y archivos a "G.C.L." en todo el proyecto.

## 5. Veredicto Técnico Final

El proyecto "G.C.L. OneStyle Mariana" presenta un estado sólido. La arquitectura de base de datos refleja coherentemente las lógicas de negocio solicitadas, la documentación gráfica de los casos de uso está bien distribuida por módulos, y los requisitos presentan trazabilidad de extremo a extremo.

**Estado para entrega final: APROBADO.**
