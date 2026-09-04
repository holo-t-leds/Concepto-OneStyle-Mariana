# G.C.C. OneStyle Mariana — Sistema de Gestión de Pedidos e Inventario (OMS)

<u>**Programa de Formación:**</u> Análisis y Desarrollo de Software (ADSO) — Código 3484008  
<u>**Fase del Proyecto:**</u> Hacer y Verificar  
<u>**Actividad de Proyecto:**</u> Desarrollar la estructura de datos y la interfaz de usuario del sistema de información  
<u>**Competencia:**</u> Evaluar requisitos de la solución de software de acuerdo con metodologías de análisis y estándares  

---

## 1. Descripción General del Proyecto

<u>**OneStyle Mariana**</u> es una plataforma web integral orientada al comercio electrónico y a la gestión operativa de pedidos (OMS) para una tienda de prendas de vestir femeninas. El sistema centraliza el catálogo público dinámico, implementa el control de inventario en tiempo real por variantes de producto (talla y color), automatiza el registro de auditoría transaccional y estructura el proceso de compra con generación de pedidos parametrizados hacia WhatsApp.

---

## 2. Arquitectura de Información y Navegación

### 2.1. Estructura Jerárquica del Sistema

El mapa de navegación define los flujos de interacción del usuario clasificados por niveles de acceso (público, autenticado y administrativo):

![Mapa de Navegacion](<docs/mapa navegacion/mapanavegacion.png>)

### 2.2. Módulos de la Solución

* <u>**Módulo de Seguridad y Usuarios (`src/auth/`):**</u> Autenticación multi-rol (`Administradora`, `Vendedora`, `Clienta`), control de sesiones, validación de credenciales con hashing seguro y recuperación de acceso.
* <u>**Módulo de Catálogo e Inventario (`src/catalogo/`):**</u> Mantenimiento de categorías maestras, gestión de existencias por variantes (talla/color) y control de alertas por punto de reposición.
* <u>**Módulo de Carrito de Compras (`src/carrito/`):**</u> Validación de disponibilidad de stock en backend, modificación de cantidades, recálculo dinámico de subtotales y vaciado controlado (`RN-CART`).
* <u>**Módulo de Pedidos y Checkout (`src/pedidos/`):**</u> Captura obligatoria de datos de despacho, cálculo del monto total y generación de enlaces de confirmación para WhatsApp.
* <u>**Módulo de Auditoría y Trazabilidad (`src/auditoria/`):**</u> Registro automático e inmutable de eventos críticos sobre precios, existencias, roles y pedidos.

---

## 3. Modelo de Datos Relacional (Base de Datos)

### 3.1. Diagrama Entidad-Relación (MER)

El esquema relacional garantiza la integridad referencial y el soporte a transacciones concurrentes:

![Modelo Entidad Relacion](<docs/ent relacion/entidad.png>)

### 3.2. Scripts SQL de Persistencia

* <u>**DDL Estructural (`database/schema.sql`):**</u> Define las tablas relacionales (`roles`, `usuarios`, `auditoria`, `categorias`, `tallas`, `colores`, `producto`, `producto_atributo`, `inventario`, `carrito`, `detalle_carrito`, `pedido`, `domicilio`, `reporte`) junto con sus llaves primarias, foráneas e índices únicos.
* <u>**Datos Semilla (`database/seeds.sql`):**</u> Carga la configuración inicial de roles de usuario y categorías base del catálogo.

---
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

---

## 4. Prototipo Interactivo y Mockups de Interfaz

### 4.1. Enlace al Prototipo Interactivo (Figma)

El diseño UI/UX del sistema se encuentra disponible para su navegación interactiva en Figma:

* <u>**Prototipo en Figma:**</u> [Ver Mockups Interactivos en Figma](https://www.figma.com/design/Ig7NbeizxVrNrnVWDm0lcA/onestyle?node-id=0-1&t=HpHegNwAzJQoyURV-1)

### 4.2. Galería de Pantallas Principales

| Vista / Interfaz | Propósito Técnico | Captura de Diseño |
| :--- | :--- | :---: |
| **Inicio de Sesión** | Acceso seguro multi-rol (`RF-003b`). | ![Inicio de Sesión](<docs/mockups/login.png>) |
| **Catálogo Dinámico** | Visualización por categorías (`RF-008`). | ![Catálogo Dinámico](<docs/mockups/catalogo.png>) |
| **Detalle de Prenda** | Selector de talla, color y stock (`RF-009`). | ![Detalle de Prenda](<docs/mockups/Detalleprenda.png>) |
| **Bolsa de Compras** | Control y vaciado de carrito (`RF-010`). | ![Bolsa de Compras](<docs/mockups/carrito.png>) |
| **Búsqueda con Éxito** | Filtro dinámico de prendas (`RF-008`). | ![Búsqueda con Éxito](<docs/mockups/busquedaexitosa.png>) |
| **Sin Resultados** | Retroalimentación de búsqueda (`RF-008`). | ![Sin Resultados](<docs/mockups/busquedasinresultados.png>) |
| **Página de Error (404)** | Manejo de rutas inexistentes (`RNF-003`). | ![Página de Error (404)](<docs/mockups/404.png>) |

### 4.3. Casos de Uso, BPMN y Diagrama de actividades
**Casos de uso**
* <u>**Documento:**</u> [Ver Casos de Uso en Google sheets](https://docs.google.com/document/d/1SimBp-0BJighWeZRdFHGI5peXwmv6t6e1VyrG6NXkP0/edit?usp=sharing)
**Diagrama de Casos de Uso:**
![Casos de Uso](<docs/Casos de uso/casosdesu.png>)

**Diagrama BPMN:**
![BPMN](<docs/Bpmn/bpmn.drawio.png>)
![BPMN](<docs/Bpmn/diagrama%20bpmn%201.png>)
![BPMN](<docs/Bpmn/diagrama%20bpmn%202.png>)
![BPMN](<docs/Bpmn/diagrama%20bpmn%203.png>)
![BPMN](<docs/Bpmn/Bpmn%20FAQ.png>)


**Diagrama de actividades:**

![diag](<docs/diagramaactividades/act%20diag.png>)

---
## 5. Matriz de Requisitos y Trazabilidad

El análisis, especificación y trazabilidad de los 38 Requisitos Funcionales (RF), Requisitos No Funcionales (RNF bajo norma ISO/IEC 25010), Criterios de Aceptación y Casos de Prueba (Caja Blanca, Caja Negra e Integración) se gestionan de manera centralizada en la hoja de cálculo oficial:

* 🔗 <u>**Enlace Oficial:**</u> [Consultar Matriz de Trazabilidad y Requisitos en Google Sheets](https://docs.google.com/spreadsheets/d/1-zfgbSbrLl8uvnGb2gGCj1UpFA3TqOewWFdeeNKSH_s/edit?usp=sharing)
* 📄 <u>**Matriz de Requisitos:**</u> [Ver documento](https://docs.google.com/spreadsheets/d/1-zfgbSbrLl8uvnGb2gGCj1UpFA3TqOewWFdeeNKSH_s/edit?usp=sharing)
---

## 6. Historias de Usuario

* 🔗 <u>**Enlace de Historias**</u> https://docs.google.com/spreadsheets/d/1xfWg9ZDWIMq2iLZ2_5q8NksZCSTSHnr9pvF7R4X3xCo/edit?usp=sharing

## 7. Estructura del Repositorio

```text
├── .github/
│   └── workflows/
│       └── tests.yml            # Pipeline de Integración Continua (CI) en GitHub Actions
├── database/
│   ├── schema.sql               # Script DDL de creación de tablas en MySQL / MariaDB
│   └── seeds.sql                # Inserción de datos maestros iniciales
├── docs/
│   ├── Bpmn/                      # Diagramas de Modelado de Procesos de Negocio
│   │   ├── Bpmn FAQ.png           # Preguntas frecuentes y guía BPMN
│   │   ├── bpmn                   # Archivo de configuración/exportación
│   │   └── bpmn.drawio.png        # Diagrama BPMN principal exportado de Draw.io
│   ├── Casos de uso/              # Modelos de Interacción del Sistema
│   │   ├── casosdesu.png          # Renderizado del Diagrama de Casos de Uso
│   │   └── casosdeuso.puml        # Código fuente PlantUML de Casos de Uso
│   ├── diagramaactividades/       # Modelos de Interacción del Sistema
│   │   ├── act diag.png           # Renderizado del Diagrama de actividades
│   │   └── actdi.puml             # Código fuente PlantUML de actividades
│   ├── ent relacion/
│   │   ├── ent.puml             # Código fuente PlantUML del Modelo Entidad-Relación
│   │   └── entidad.png          # Renderizado visual del MER
│   ├── mapa navegacion/
│   │   ├── mapnav.puml          # Código fuente PlantUML de navegación (Mindmap)
│   │   └── mapanavegacion.png   # Renderizado visual del mapa de navegación
│   └── mockups/                 # Diseños de alta fidelidad exportados de Figma
│   │   ├── 404.png
│   │   ├── Detalleprenda.png
│   │   ├── Html.png
│   │   ├── busquedaexitosa.png
│   │   ├── busquedasinresultados.png
│   │   ├── carrito.png
│   │   ├── catalogo.png
│   │   └── login.png
│   └── board.jpg                 # Imagen Storyboard
├── src/
│   ├── __init__.py
│   ├── auditoria/               # Lógica de trazas y logs transaccionales
│   │   └── service.py
│   ├── auth/                    # Lógica de usuarios, roles y autenticación
│   │   └── service.py
│   ├── carrito/                 # Lógica de control de carrito y validación de stock
│   │   └── service.py
│   ├── catalogo/                # Lógica de productos, variantes y existencias
│   │   └── service.py
│   ├── modulos/                 # Prototipos visuales y referencias gráficas
│   │   └── prototipo_catalogo_inventario.html
│   └── pedidos/                 # Lógica de pedidos, totalización y WhatsApp
│       └── service.py
├── tests/
│   ├── __init__.py
│   └── unit/                    # Suite de pruebas unitarias (Mindset TDD)
│       ├── test_auth.py
│       ├── test_carrito.py
│       └── test_pedidos.py
├── .gitignore
├── Matriz de requisitos         # Enlace directo a la Matriz de Trazabilidad
├── requirements.txt             # Dependencias del proyecto (pytest)
└── README.md                    # Documentación técnica oficial
