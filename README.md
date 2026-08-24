# Concepto OneStyle - Mariana

Descripción
-----------
Este repositorio contiene los recursos y el desarrollo del reto "Arquitecto de Soluciones" correspondiente al módulo 3.2: Modelado y Lógica. Su propósito es documentar y ejemplificar enfoques de modelado, razonamiento y diseño de soluciones que simulen o representen principios de ingeniería del conocimiento (la denominada "Ingeniería del Cerebro").

Lenguaje principal
------------------
Python, SQL

Objetivos
---------
- Documentar el enfoque conceptual y las decisiones de modelado.
- Proveer ejemplos y plantillas que ilustren patrones de lógica y arquitectura.

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas principales:

- `database/`: Contiene los scripts DDL de la base de datos MySQL/MariaDB (`schema.sql`) y los datos iniciales (`seeds.sql`).
- `src/`: Contiene los módulos principales de lógica de negocio escritos en Python:
  - `auth/`: Autenticación de usuarios y roles.
  - `catalogo/`: Gestión de productos, variantes e inventario.
  - `carrito/`: Gestión del carrito de compras y validaciones de stock.
  - `pedidos/`: Creación de pedidos y generación de enlaces de WhatsApp.
  - `auditoria/`: Registro de logs de acciones importantes.
- `tests/`: Pruebas unitarias para los módulos Python utilizando `pytest`.
- `docs/`: Documentación y diagramas del proyecto.

## Instrucciones de Uso

### 1. Base de Datos

Para inicializar la base de datos, ejecuta los siguientes scripts SQL en tu servidor MySQL/MariaDB:

1. Estructura de tablas: `mysql -u usuario -p base_de_datos < database/schema.sql`
2. Datos iniciales: `mysql -u usuario -p base_de_datos < database/seeds.sql`

### 2. Entorno y Pruebas Locales (TDD)

El proyecto utiliza `pytest` para las pruebas unitarias. Para ejecutarlas:

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta los tests:
   ```bash
   PYTHONPATH=. pytest tests/
   ```

El proyecto también incluye un flujo de trabajo CI (`.github/workflows/tests.yml`) para ejecutar automáticamente estas pruebas en cada push o pull request.

## Modelo Entidad-Relación

A continuación se presenta el diseño de la base de datos para el proyecto:

![Diagrama Entidad Relacion](./docs/ent%20relacion/entidad.png)
