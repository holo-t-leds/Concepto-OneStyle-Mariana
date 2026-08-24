-- Default data seeds for roles and master categories

INSERT INTO roles (nombre_rol) VALUES
('Administradora'),
('Vendedora'),
('Clienta');

INSERT INTO categorias (nombre_categoria, descripcion_categoria) VALUES
('Blusas', 'Blusas de diferentes estilos y materiales'),
('Pantalones', 'Pantalones casuales y formales'),
('Vestidos', 'Vestidos para cualquier ocasión'),
('Chaquetas', 'Chaquetas y abrigos');

INSERT INTO tallas (nombre_talla) VALUES
('XS'),
('S'),
('M'),
('L'),
('XL');

INSERT INTO colores (nombre_color) VALUES
('Blanco'),
('Negro'),
('Rojo'),
('Azul'),
('Verde');
