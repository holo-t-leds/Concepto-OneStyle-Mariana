-- MySQL/MariaDB DDL Schema
-- Based on the requirements and ent.puml

CREATE TABLE IF NOT EXISTS roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_rol INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    estado_usuario BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_id_rol) REFERENCES roles(id_rol)
);

CREATE TABLE IF NOT EXISTS auditoria (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_usuario_accion INT NOT NULL,
    tipo_accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(100) NOT NULL,
    id_registro_afectado INT,
    valor_anterior TEXT,
    valor_nuevo TEXT,
    fecha_accion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_id_usuario_accion) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL UNIQUE,
    descripcion_categoria TEXT,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS tallas (
    id_talla INT AUTO_INCREMENT PRIMARY KEY,
    nombre_talla VARCHAR(10) NOT NULL UNIQUE,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS colores (
    id_color INT AUTO_INCREMENT PRIMARY KEY,
    nombre_color VARCHAR(50) NOT NULL UNIQUE,
    codigo_hex VARCHAR(10),
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_categoria INT NOT NULL,
    nombre_producto VARCHAR(150) NOT NULL,
    descripcion_producto TEXT,
    precio_detallista DECIMAL(12,2) NOT NULL,
    url_imagen_principal VARCHAR(255),
    estado_visibilidad BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (fk_id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE IF NOT EXISTS producto_imagen (
    id_imagen INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_producto INT NOT NULL,
    url_imagen VARCHAR(255) NOT NULL,
    formato VARCHAR(10),
    es_principal BOOLEAN DEFAULT FALSE,
    fecha_carga DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE IF NOT EXISTS producto_atributo (
    id_variante INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_producto INT NOT NULL,
    fk_id_talla INT NOT NULL,
    fk_id_color INT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (fk_id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (fk_id_talla) REFERENCES tallas(id_talla),
    FOREIGN KEY (fk_id_color) REFERENCES colores(id_color)
);

CREATE TABLE IF NOT EXISTS inventario (
    id_inventario INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_variante INT NOT NULL,
    stock_disponible INT NOT NULL DEFAULT 0,
    punto_reposicion INT NOT NULL DEFAULT 5,
    FOREIGN KEY (fk_id_variante) REFERENCES producto_atributo(id_variante)
);

CREATE TABLE IF NOT EXISTS carrito (
    id_carrito INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_usuario INT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS detalle_carrito (
    id_detalle_carrito INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_carrito INT NOT NULL,
    fk_id_variante INT NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(12,2),
    subtotal DECIMAL(12,2),
    cantidad_reservada INT DEFAULT 0,
    fecha_expiracion DATETIME,
    FOREIGN KEY (fk_id_carrito) REFERENCES carrito(id_carrito),
    FOREIGN KEY (fk_id_variante) REFERENCES producto_atributo(id_variante)
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_usuario INT NOT NULL,
    fk_id_vendedora_asig INT,
    estado_pedido VARCHAR(50) NOT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATETIME,
    total_pedido DECIMAL(12,2) NOT NULL,
    url_comprobante_whatsapp VARCHAR(255),
    FOREIGN KEY (fk_id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (fk_id_vendedora_asig) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id_detalle_pedido INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_pedido INT NOT NULL,
    fk_id_variante INT NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (fk_id_pedido) REFERENCES pedido(id_pedido),
    FOREIGN KEY (fk_id_variante) REFERENCES producto_atributo(id_variante)
);

CREATE TABLE IF NOT EXISTS historial_pedido (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_pedido INT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_id_pedido) REFERENCES pedido(id_pedido)
);

CREATE TABLE IF NOT EXISTS domicilio (
    id_domicilio INT AUTO_INCREMENT PRIMARY KEY,
    fk_id_pedido INT NOT NULL,
    direccion_envio TEXT NOT NULL,
    barrio VARCHAR(100),
    ciudad VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    observaciones TEXT,
    FOREIGN KEY (fk_id_pedido) REFERENCES pedido(id_pedido)
);

CREATE TABLE IF NOT EXISTS categorias_faq (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS faq (
    id_faq INT AUTO_INCREMENT PRIMARY KEY,
    id_categoria INT NOT NULL,
    pregunta VARCHAR(255) NOT NULL,
    respuesta TEXT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    orden INT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_actualizacion INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias_faq(id_categoria),
    FOREIGN KEY (usuario_actualizacion) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS configuracion_soporte (
    id_contacto INT AUTO_INCREMENT PRIMARY KEY,
    tipo_contacto VARCHAR(50) NOT NULL,
    destino VARCHAR(255) NOT NULL,
    horario_atencion VARCHAR(255),
    mensaje_predeterminado TEXT,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS reporte (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_reporte VARCHAR(150) NOT NULL,
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    periodo_inicio DATETIME,
    periodo_fin DATETIME,
    descripcion TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
