
# 3.3 Diccionario de Datos — G.C.C. OneStyle Mariana (OMS)

**Sistema de Gestión de Pedidos e Inventario**  
**Programa de Formación:** Análisis y Desarrollo de Software (ADSO)  
**Fase del Proyecto:** Hacer y Verificar  

---

## 3.4 Introducción y Convenciones del Modelo
Este diccionario de datos detalla la totalidad de las entidades físicas implementadas en el script `database/schema.sql` y representadas en el Modelo Entidad-Relación (`docs/Casos de uso/ent.puml`). Describe las claves primarias (PK), foráneas (FK), tipos de datos, restricciones de nulidad y el propósito operativo de cada campo conforme a los Requisitos de Información (RI) de la Matriz del proyecto.

### Convenciones:
* **PK:** Llave Primaria (*Primary Key*). Identificador unívoco de la tupla.
* **FK:** Llave Foránea (*Foreign Key*). Representa la integridad referencial.
* **Nulo (No):** Atributo obligatorio (`NOT NULL`).
* **Nulo (Sí):** Atributo opcional o condicionado por el flujo de negocio.

---

## 3.5 Especificación Detallada de Tablas

### 3.5.1. Tabla: `roles`
**Propósito de la Entidad:** Almacena los perfiles de acceso y permisos del sistema (Administradora, Vendedora, Clienta).

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_rol` | INT | PK | No | Identificador único autoincremental del rol. |
| `nombre_rol` | VARCHAR(50) | - | No | Nombre identificador único del rol (Administradora, Vendedora, Clienta). |

---

### 3.5.2. Tabla: `usuarios`
**Propósito de la Entidad:** Gestiona las cuentas de acceso, credenciales autenticables y roles asignados a los usuarios de la plataforma.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_usuario` | INT | PK | No | Identificador único autoincremental del usuario. |
| `fk_id_rol` | INT | FK | No | Llave foránea que referencia a roles(id_rol). Define los permisos del usuario. |
| `nombre` | VARCHAR(100) | - | No | Nombre de pila del usuario registrado. |
| `apellido` | VARCHAR(100) | - | No | Apellido del usuario registrado. |
| `email` | VARCHAR(150) | - | No | Correo electrónico único utilizado como identificador de inicio de sesión. |
| `contrasena` | VARCHAR(255) | - | No | Contraseña encriptada bajo algoritmo robusto (bcrypt). |
| `telefono` | VARCHAR(20) | - | Sí | Número telefónico o de contacto del usuario. |
| `estado_usuario` | BOOLEAN | - | No | Estado lógico del usuario (TRUE = Activo, FALSE = Inactivo/Baja lógica). Default TRUE. |
| `fecha_registro` | DATETIME | - | No | Marca temporal de registro inicial en la plataforma. Default CURRENT_TIMESTAMP. |

---

### 3.5.3. Tabla: `auditoria`
**Propósito de la Entidad:** Trazabilidad transaccional inmutable de operaciones críticas sobre stock, precios, usuarios y catálogo.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_log` | INT | PK | No | Identificador único autoincremental del registro de auditoría. |
| `fk_id_usuario_accion` | INT | FK | No | Llave foránea hacia usuarios(id_usuario) que ejecutó la operación. |
| `tipo_accion` | VARCHAR(100) | - | No | Tipo de acción ejecutada (ej. INSERT, UPDATE, DELETE_LOGICO, CAMBIO_STOCK). |
| `tabla_afectada` | VARCHAR(100) | - | No | Nombre de la entidad física de base de datos impactada por el cambio. |
| `id_registro_afectado` | INT | - | Sí | Identificador de la tupla impactada en la tabla afectada. |
| `valor_anterior` | TEXT | - | Sí | Estado previo del dato en formato JSON o serializado antes de la mutación. |
| `valor_nuevo` | TEXT | - | Sí | Estado actualizado del dato en formato JSON o serializado tras la mutación. |
| `fecha_accion` | DATETIME | - | No | Fecha y hora exacta en que se ejecutó la acción. Default CURRENT_TIMESTAMP. |

---

### 3.5.4. Tabla: `categorias`
**Propósito de la Entidad:** Clasifica y organiza jerárquicamente las prendas dentro del catálogo público.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_categoria` | INT | PK | No | Identificador único autoincremental de la categoría. |
| `nombre_categoria` | VARCHAR(100) | - | No | Nombre comercial único de la categoría (ej. Blusas, Vestidos, Pantalones). |
| `descripcion_categoria` | TEXT | - | Sí | Descripción detallada del tipo de prendas agrupadas. |
| `estado` | BOOLEAN | - | No | Estado lógico de visualización pública (TRUE = Activa, FALSE = Inactiva). Default TRUE. |

---

### 3.5.5. Tabla: `tallas`
**Propósito de la Entidad:** Tabla maestra de dimensiones físicas estandarizadas para las prendas de vestir.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_talla` | INT | PK | No | Identificador único autoincremental de la talla. |
| `nombre_talla` | VARCHAR(10) | - | No | Identificador textual único de la talla (ej. XS, S, M, L, XL). |
| `estado` | BOOLEAN | - | No | Disponibilidad de la talla para nuevas variantes (TRUE = Activa, FALSE = Inactiva). Default TRUE. |

---

### 3.5.6. Tabla: `colores`
**Propósito de la Entidad:** Tabla maestra de tonalidades disponibles para las variantes de prendas.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_color` | INT | PK | No | Identificador único autoincremental del color. |
| `nombre_color` | VARCHAR(50) | - | No | Nombre comercial único del color (ej. Negro, Blanco, Vinotinto). |
| `codigo_hex` | VARCHAR(10) | - | Sí | Código hexadecimal del color para renderizado gráfico en la interfaz (ej. #000000). |
| `estado` | BOOLEAN | - | No | Disponibilidad del color (TRUE = Activo, FALSE = Inactivo). Default TRUE. |

---

### 3.5.7. Tabla: `producto`
**Propósito de la Entidad:** Almacena la ficha base de las prendas ofertadas en el catálogo.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_producto` | INT | PK | No | Identificador único autoincremental de la prenda/producto. |
| `fk_id_categoria` | INT | FK | No | Llave foránea que referencia a categorias(id_categoria). |
| `nombre_producto` | VARCHAR(150) | - | No | Nombre comercial descriptivo de la prenda. |
| `descripcion_producto` | TEXT | - | Sí | Descripción ampliada de materiales, diseño, horma y especificaciones. |
| `precio_detallista` | DECIMAL(12,2) | - | No | Precio de venta unitario detallista en moneda local (COP). |
| `url_imagen_principal` | VARCHAR(255) | - | Sí | URL o ruta relativa de la imagen destacada en el catálogo. |
| `estado_visibilidad` | BOOLEAN | - | No | Control de visibilidad pública (TRUE = Visible en tienda, FALSE = Oculto). Default TRUE. |

---

### 3.5.8. Tabla: `producto_imagen`
**Propósito de la Entidad:** Gestiona la galería multimedia complementaria de 1 a N imágenes por prenda.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_imagen` | INT | PK | No | Identificador único autoincremental de la imagen de soporte. |
| `fk_id_producto` | INT | FK | No | Llave foránea que asocia la imagen a producto(id_producto). |
| `url_imagen` | VARCHAR(255) | - | No | Ruta de almacenamiento local o URL en CDN del recurso gráfico. |
| `formato` | VARCHAR(10) | - | Sí | Extensión o formato MIME de la imagen (ej. WEBP, PNG, JPG). |
| `es_principal` | BOOLEAN | - | No | Indicador booleano (TRUE = Imagen de portada, FALSE = Imagen secundaria). Default FALSE. |
| `fecha_carga` | DATETIME | - | No | Marca temporal de carga del archivo al sistema. Default CURRENT_TIMESTAMP. |

---

### 3.5.9. Tabla: `producto_atributo`
**Propósito de la Entidad:** Entidad asociativa que descompone la relación N:M entre producto, tallas y colores, definiendo las variantes SKU.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_variante` | INT | PK | No | Identificador único autoincremental de la combinación de atributos (variante). |
| `fk_id_producto` | INT | FK | No | Llave foránea hacia producto(id_producto). |
| `fk_id_talla` | INT | FK | No | Llave foránea hacia tallas(id_talla). |
| `fk_id_color` | INT | FK | No | Llave foránea hacia colores(id_color). |
| `estado` | BOOLEAN | - | No | Disponibilidad comercial de la variante (TRUE = Activa, FALSE = Descontinuada). Default TRUE. |

---

### 3.5.10. Tabla: `inventario`
**Propósito de la Entidad:** Control de existencias físicas y umbrales de reabastecimiento por cada variante de producto.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_inventario` | INT | PK | No | Identificador único autoincremental del registro de stock. |
| `fk_id_variante` | INT | FK | No | Llave foránea única hacia producto_atributo(id_variante). Relación 1:1. |
| `stock_disponible` | INT | - | No | Cantidad física real en bodega apta para venta inmediata. Default 0. |
| `punto_reposicion` | INT | - | No | Nivel mínimo de existencias para detonar alertas de compra preventiva. Default 5. |

---

### 3.5.11. Tabla: `carrito`
**Propósito de la Entidad:** Contenedor transaccional temporal de selección de compra asociado a un usuario.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_carrito` | INT | PK | No | Identificador único autoincremental del carrito de compras. |
| `fk_id_usuario` | INT | FK | No | Llave foránea hacia usuarios(id_usuario) propietario de la sesión de compra. |
| `fecha_creacion` | DATETIME | - | No | Marca temporal de creación del carrito. Default CURRENT_TIMESTAMP. |

---

### 3.5.12. Tabla: `detalle_carrito`
**Propósito de la Entidad:** Líneas de prendas añadidas al carrito con control dinámico de precios y reservas temporales.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_detalle_carrito` | INT | PK | No | Identificador único autoincremental del ítem dentro del carrito. |
| `fk_id_carrito` | INT | FK | No | Llave foránea que referencia a carrito(id_carrito). |
| `fk_id_variante` | INT | FK | No | Llave foránea que referencia a producto_atributo(id_variante). |
| `cantidad` | INT | - | No | Unidades seleccionadas por la clienta para comprar. |
| `precio` | DECIMAL(12,2) | - | Sí | Precio unitario fijado al momento de añadir al carrito. |
| `subtotal` | DECIMAL(12,2) | - | Sí | Monto calculado resultante (cantidad * precio). |
| `cantidad_reservada` | INT | - | Sí | Existencias retenidas provisionalmente para prevenir colisiones de stock. Default 0. |
| `fecha_expiracion` | DATETIME | - | Sí | Tiempo límite de retención antes de retornar el stock reservado a disponible. |

---

### 3.5.13. Tabla: `pedido`
**Propósito de la Entidad:** Cabecera transaccional que formaliza la orden de compra y canaliza el cierre comercial vía WhatsApp.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_pedido` | INT | PK | No | Identificador único autoincremental del pedido. |
| `fk_id_usuario` | INT | FK | No | Llave foránea hacia usuarios(id_usuario) que realizó la compra (Clienta). |
| `fk_id_vendedora_asig` | INT | FK | Sí | Llave foránea hacia usuarios(id_usuario) que gestiona y asesora el pedido (Vendedora). |
| `estado_pedido` | VARCHAR(50) | - | No | Estado logístico actual (Pendiente de Pago, Confirmado, En Empaque, Despachado, Entregado, Cancelado). |
| `fecha_pedido` | DATETIME | - | No | Marca temporal de confirmación del pedido. Default CURRENT_TIMESTAMP. |
| `fecha_entrega` | DATETIME | - | Sí | Fecha y hora pactada o efectiva de entrega de la mercancía. |
| `total_pedido` | DECIMAL(12,2) | - | No | Importe total consolidado a pagar por la clienta. |
| `url_comprobante_whatsapp` | VARCHAR(255) | - | Sí | Enlace o referencia al comprobante de pago enviado por chat. |

---

### 3.5.14. Tabla: `detalle_pedido`
**Propósito de la Entidad:** Desglose histórico inmutable de los productos y precios facturados en cada pedido.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_detalle_pedido` | INT | PK | No | Identificador único autoincremental de la línea facturada. |
| `fk_id_pedido` | INT | FK | No | Llave foránea hacia la orden principal en pedido(id_pedido). |
| `fk_id_variante` | INT | FK | No | Llave foránea hacia producto_atributo(id_variante). |
| `cantidad` | INT | - | No | Cantidad definitiva de unidades adquiridas y descontadas del inventario. |
| `precio` | DECIMAL(12,2) | - | No | Precio histórico de venta al momento de cerrar la transacción. |

---

### 3.5.15. Tabla: `historial_pedido`
**Propósito de la Entidad:** Registro cronológico de las transiciones de estado para auditoría y rastreo de envíos.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_historial` | INT | PK | No | Identificador único autoincremental del evento de transición. |
| `fk_id_pedido` | INT | FK | No | Llave foránea vinculada a pedido(id_pedido). |
| `estado` | VARCHAR(50) | - | No | Estado al cual transitó la orden en dicho evento. |
| `fecha_hora` | DATETIME | - | No | Marca temporal exacta del cambio de estado. Default CURRENT_TIMESTAMP. |

---

### 3.5.16. Tabla: `domicilio`
**Propósito de la Entidad:** Estructura los datos de destino físico y logística de entrega asociados a una orden.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_domicilio` | INT | PK | No | Identificador único autoincremental del registro de entrega. |
| `fk_id_pedido` | INT | FK | No | Llave foránea que asocia los datos de despacho con pedido(id_pedido). |
| `direccion_envio` | TEXT | - | No | Nomenclatura física detallada del domicilio de entrega. |
| `barrio` | VARCHAR(100) | - | Sí | Barrio o sector específico del despacho. |
| `ciudad` | VARCHAR(100) | - | No | Ciudad o municipio de entrega. |
| `telefono` | VARCHAR(20) | - | Sí | Número de contacto para coordinar la entrega con la clienta. |
| `observaciones` | TEXT | - | Sí | Instrucciones logísticas especiales (ej. conjunto cerrado, torre, apto). |

---

### 3.5.17. Tabla: `categorias_faq`
**Propósito de la Entidad:** Agrupación temática para estructurar las dudas y preguntas frecuentes de los clientes.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_categoria` | INT | PK | No | Identificador único autoincremental de la categoría temática. |
| `nombre_categoria` | VARCHAR(100) | - | No | Nombre de la sección de ayuda (ej. Envíos, Pagos, Tallas y Medidas). |
| `estado` | BOOLEAN | - | No | Visibilidad de la categoría en el centro de ayuda (TRUE = Activa, FALSE = Oculta). Default TRUE. |

---

### 3.5.18. Tabla: `faq`
**Propósito de la Entidad:** Repositorio centralizado de respuestas oficiales y preguntas frecuentes del negocio.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_faq` | INT | PK | No | Identificador único autoincremental de la pregunta frecuente. |
| `id_categoria` | INT | FK | No | Llave foránea hacia categorias_faq(id_categoria). |
| `pregunta` | VARCHAR(255) | - | No | Texto o enunciado interrogativo de la duda recurrente. |
| `respuesta` | TEXT | - | No | Contenido resolutivo detallado para orientar a la clienta. |
| `estado` | BOOLEAN | - | No | Control de publicación en la vista pública. Default TRUE. |
| `orden` | INT | - | Sí | Posición numérica secuencial para organizar la visualización en la interfaz. |
| `fecha_creacion` | DATETIME | - | No | Marca temporal de alta del registro. Default CURRENT_TIMESTAMP. |
| `fecha_actualizacion` | DATETIME | - | No | Marca temporal de última modificación. ON UPDATE CURRENT_TIMESTAMP. |
| `usuario_actualizacion` | INT | FK | Sí | Llave foránea hacia usuarios(id_usuario) que realizó la última edición. |

---

### 3.5.19. Tabla: `configuracion_soporte`
**Propósito de la Entidad:** Parámetros y canales oficiales de asistencia personalizada para escalamiento de incidencias.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_contacto` | INT | PK | No | Identificador único autoincremental del canal de contacto. |
| `tipo_contacto` | VARCHAR(50) | - | No | Tipo de vía de atención (ej. WhatsApp Asesoría, Email Soporte). |
| `destino` | VARCHAR(255) | - | No | Destino técnico (enlace URL directo, número telefónico o dirección de correo). |
| `horario_atencion` | VARCHAR(255) | - | Sí | Ventana de disponibilidad de atención al público. |
| `mensaje_predeterminado` | TEXT | - | Sí | Plantilla de texto inicial con la que se pre-diligencia el chat de soporte. |
| `estado` | BOOLEAN | - | No | Disponibilidad del canal (TRUE = Habilitado, FALSE = Deshabilitado). Default TRUE. |

---

### 3.5.20. Tabla: `reporte`
**Propósito de la Entidad:** Consolida los metadatos e indicadores de gestión gerencial exportables por la administradora.

| Nombre del Campo | Tipo de Dato | Clave | Permite Nulos | Descripción del Atributo |
| :--- | :--- | :---: | :---: | :--- |
| `id_reporte` | INT | PK | No | Identificador único autoincremental del reporte generado. |
| `id_usuario` | INT | FK | No | Llave foránea hacia usuarios(id_usuario) de rol administrativo que generó el informe. |
| `tipo_reporte` | VARCHAR(150) | - | No | Clasificación métrica (ej. Ventas por Vendedora, Rotación de Prendas, Stock Crítico). |
| `fecha_generacion` | DATETIME | - | No | Marca temporal de emisión del reporte. Default CURRENT_TIMESTAMP. |
| `periodo_inicio` | DATETIME | - | Sí | Fecha y hora inicial del filtro de datos consolidado. |
| `periodo_fin` | DATETIME | - | Sí | Fecha y hora de corte del filtro de datos consolidado. |
| `descripcion` | TEXT | - | Sí | Resumen ejecutivo, filtros aplicados y observaciones del informe. |
