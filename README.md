# G.C.C. OneStyle Mariana — Sistema de Gestión de Pedidos e Inventario (OMS)

<u>**Programa de Formación:**</u> Análisis y Desarrollo de Software (ADSO) — Código 228118  
<u>**Fase del Proyecto:**</u> Hacer y Verificar  
<u>**Actividad de Proyecto:**</u> Desarrollar la estructura de datos y la interfaz de usuario del sistema de información[cite: 1]  
<u>**Competencia:**</u> Evaluar requisitos de la solución de software de acuerdo con metodologías de análisis y estándares[cite: 1]  

---

## 1. Descripción del Proyecto

<u>**OneStyle Mariana**</u> es una solución tecnológica diseñada para optimizar y automatizar el flujo operativo de venta, control de inventario y atención a clientes de una tienda de prendas de vestir femeninas. El sistema reemplaza la gestión manual tradicional a través de redes sociales por una plataforma estructurada que centraliza el catálogo público, gestiona pedidos con enlace parametrizado a WhatsApp, controla existencias por variantes compuestas (Talla/Color) y proporciona un panel administrativo con trazabilidad y auditoría integral.

---

## 2. Arquitectura de Información y Navegación

### 2.1. Mapa de Navegación del Sistema

A continuación se presenta la estructura jerárquica de vistas y accesos correspondiente a la arquitectura de información del aplicativo:

![Mapa de Navegación](docs/mapa%20navegacion/mapanavegacion.png)

### 2.2. Módulos Funcionales

El sistema se estructura en <u>5 módulos funcionales</u> con cobertura total de los 38 requerimientos técnicos levantados:

* <u>**Seguridad y Usuarios:**</u> Autenticación multi-rol (Administradora, Vendedora, Clienta), encriptación con bcrypt, recuperación temporal de credenciales y registro inmutable de auditoría transaccional.
* <u>**Catálogo e Inventario:**</u> Clasificación por categorías, control de variantes de producto (tallas y colores maestros), alertas automáticas por punto de reposición y borrado lógico.
* <u>**Carrito de Compras:**</u> Validación de existencias en tiempo real desde el backend, recálculo dinámico de subtotales y captura obligatoria de datos de despacho previa al checkout.
* <u>**Pedidos y Gestión (OMS):**</u> Control de transiciones del ciclo de vida del pedido, generación de enlaces directos a WhatsApp para confirmación de pago y métricas de gestión.
* <u>**Soporte y FAQ:**</u> Módulo informativo de autogestión para clientas con clasificación por temas y canales de contacto directo.

---

## 3. Modelo de Datos Relacional

### 3.1. Diagrama Entidad-Relación (MER)

El modelo relacional está estructurado para soportar transacciones concurrentes sin inconsistencias de stock, preservando la integridad referencial histórica mediante estados lógicos:

![Modelo Entidad Relacion](docs/ent%20relacion/entidad.png)

### 3.2. Entidades Principales

* <u>**Módulo de Usuarios:**</u> `roles`, `usuarios`, `auditoria`, `reporte`.
* <u>**Módulo de Catálogo:**</u> `categorias`, `tallas`, `colores`, `producto`, `producto_atributo`, `inventario`[cite: 2].
* <u>**Módulo de Transacciones:**</u> `carrito`, `detalle_carrito`, `pedido`, `domicilio`[cite: 2].

---

## 4. Algoritmos y Lógica de Negocio

El repositorio contiene las implementaciones de lógica preliminar en pseudocódigo (PSeInt) que definen las reglas de negocio críticas:

* <u>**Validación de Inventario (`src/modulos/stick.psc`):**</u> Algoritmo que valida la cantidad solicitada contra el stock disponible antes de admitir cualquier operación de decremento o venta.
* <u>**Flujo de Checkout y Reserva (`src/modulos/Stock2`):**</u> Procesa la captura de datos del cliente, evalúa la disponibilidad de la prenda y genera la respuesta para el enlace parametrizado de WhatsApp.

---

## 5. Estructura del Repositorio

```text
├── docs/
│   ├── ent relacion/
│   │   ├── ent.puml                 # Código fuente PlantUML del Modelo Entidad-Relación
│   │   └── entidad.png              # Renderizado visual del diagrama MER
│   └── mapa navegacion/
│       ├── mapnav.puml              # Código fuente PlantUML del mapa de navegación
│       └── mapanavegacion.png       # Renderizado visual del mapa de navegación
├── src/
│   └── modulos/
│       ├── stick.psc                # Algoritmo en PSeInt: Control y validación de stock
│       └── Stock2                   # Algoritmo en PSeInt: Reserva de pedido y enlace WhatsApp
├── Matriz de requisitos             # Enlace a la Matriz de Trazabilidad y Requisitos en Google Sheets
└── README.md                        # Documentación técnica general del proyecto
