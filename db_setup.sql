-- Crear la base de datos
DROP DATABASE IF EXISTS tiendajohana_db;
CREATE DATABASE IF NOT EXISTS tiendajohana_db;
USE tiendajohana_db;

-- Tabla de Categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Productos (mejorada)
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria_id INT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_compra DECIMAL(10, 2),
    precio_venta DECIMAL(10, 2) NOT NULL,
    imagen TEXT,
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 0,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    color VARCHAR(30),
    talla VARCHAR(20),
    garantia_dias INT,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- Tabla de Usuarios (mejorada)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    correo VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('cliente', 'administrador', 'empleado') DEFAULT 'cliente',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL
);

-- Tabla de Direcciones
CREATE TABLE IF NOT EXISTS direcciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    direccion VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    estado VARCHAR(100),
    codigo_postal VARCHAR(20),
    pais VARCHAR(100) NOT NULL,
    tipo ENUM('facturacion', 'envio') DEFAULT 'envio',
    principal BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de Carrito (mejorada)
CREATE TABLE IF NOT EXISTS carrito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    producto_id INT,
    cantidad INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    UNIQUE KEY unique_usuario_producto (usuario_id, producto_id)
);

-- Tabla de Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    numero_pedido VARCHAR(50) UNIQUE NOT NULL,
    estado ENUM('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado') DEFAULT 'pendiente',
    subtotal DECIMAL(10, 2) NOT NULL,
    impuestos DECIMAL(10, 2) DEFAULT 0,
    gastos_envio DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    metodo_pago VARCHAR(50),
    direccion_envio_id INT,
    direccion_facturacion_id INT,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_envio TIMESTAMP NULL,
    fecha_entrega TIMESTAMP NULL,
    notas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (direccion_envio_id) REFERENCES direcciones(id) ON DELETE SET NULL,
    FOREIGN KEY (direccion_facturacion_id) REFERENCES direcciones(id) ON DELETE SET NULL
);

-- Tabla de Detalles del Pedido
CREATE TABLE IF NOT EXISTS pedido_detalles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    producto_id INT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL
);

-- Tabla de Movimientos de Inventario
CREATE TABLE IF NOT EXISTS inventario_movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    tipo ENUM('entrada', 'salida') NOT NULL,
    cantidad INT NOT NULL,
    motivo VARCHAR(100),
    referencia_tipo ENUM('compra', 'venta', 'ajuste', 'devolucion'),
    referencia_id INT,
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);

-- Tabla de Pagos
CREATE TABLE IF NOT EXISTS pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    monto DECIMAL(10, 2) NOT NULL,
    metodo_pago ENUM('tarjeta_credito', 'tarjeta_debito', 'transferencia', 'efectivo', 'paypal') NOT NULL,
    estado ENUM('pendiente', 'completado', 'fallido', 'reembolsado') DEFAULT 'pendiente',
    transaction_id VARCHAR(100),
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE
);

-- Tabla de Descuentos/Cupones
CREATE TABLE IF NOT EXISTS cupones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    tipo_descuento ENUM('porcentaje', 'fijo') NOT NULL,
    valor_descuento DECIMAL(10, 2) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    usos_maximos INT DEFAULT 0, -- 0 para ilimitados
    usos_actuales INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Reseñas de Productos
CREATE TABLE IF NOT EXISTS reseñas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    usuario_id INT,
    calificacion INT CHECK (calificacion >= 1 AND calificacion <= 5),
    comentario TEXT,
    fecha_resena TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY unique_usuario_producto_resena (usuario_id, producto_id)
);

-- Tabla de Lista de Deseos
CREATE TABLE IF NOT EXISTS lista_deseos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    producto_id INT,
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    UNIQUE KEY unique_usuario_producto_deseos (usuario_id, producto_id)
);

-- =========================================================================
-- DATOS SEMILLA (Para pruebas de la tienda con la estructura profesional)
-- =========================================================================

-- Limpiar datos previos si existen (en orden inverso de dependencias)
DELETE FROM productos;
DELETE FROM categorias;

-- Insertar Categorías principales
INSERT INTO categorias (id, nombre, descripcion) VALUES
(1, 'Electrónica', 'Dispositivos tecnológicos, laptops, auriculares, etc.'),
(2, 'Ropa', 'Prendas de vestir exclusivas y calzado de calidad'),
(3, 'General', 'Productos varios del catálogo general');

-- Insertar Productos semilla
INSERT INTO productos (nombre, categoria_id, descripcion, precio_compra, precio_venta, imagen, stock_actual, stock_minimo, marca, modelo, color, talla, garantia_dias, estado) VALUES
('Laptop ASUS ROG Strix', 1, 'Laptop gamer de alto rendimiento con procesador potente y tarjeta de video de última generación.', 800.00, 1200.00, 'https://lh3.googleusercontent.com/aida-public/AB6AXuA30YL-762rnLpfu_NwhuUo0NEiwr08VlcxZoRAnCj_09sBn0wObWEVZpEnGZcsJl4Ld60dbgRBjBfJT6kL4EKLa-6CqfikZOuNxXy1QN1knSoLKbcRTLDIkdaIbIp_sTierqzkVql8gKOk-YAIoL0RBvyzy8vXDOEAm3xpB4ZSDyyo-UnY64rOJrU_K52xIolRP2jTb0ul1CYbniFK9bGV1OjRgz_GYNOVgJOPxNryAAS7UE0f_zbf5sEV3FJNOIQ1EqUEzeDXGJM', 15, 3, 'ASUS', 'ROG Strix G15', 'Gris Eclipse', NULL, 365, 'activo'),
('Auriculares Sony WH-1000XM4', 1, 'Auriculares inalámbricos de diadema con cancelación de ruido premium y sonido de alta resolución.', 180.00, 299.99, 'https://lh3.googleusercontent.com/aida-public/AB6AXuDtKGsfNkJ4SQV26YNDy7XlYLoV_2f0cqlQ17jD-6Dc9CzzTJRmUWHSvzxI3VAw6j8e38NAktBVRxnVt_RozfNUxfU4hmmWYal06Kdl7nJh0hP8E6w7ws19N6UWAGAec1KYZ-UBE5xgGb8Tyv6bUNGRsLdBEsVmgySc-t5OHLPqxQDBQWd18tTQyu6ESbqfyvKIydQfsa0vYXxHalYAZqgw37u8bFU-dAwl1jQSMN9IyRTqxBH1xLevfjozKJSNCRTvaAKikUSLxRA', 25, 5, 'Sony', 'WH-1000XM4', 'Negro', NULL, 180, 'activo'),
('Chaqueta de Cuero Premium', 2, 'Chaqueta de cuero sintético estilo Biker de corte moderno, resistente al viento y muy elegante.', 45.00, 89.99, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?q=80&w=600&auto=format&fit=crop', 40, 8, 'Zara', 'Biker Classic', 'Negro', 'L', NULL, 'activo'),
('Camiseta de Algodón Orgánico', 2, 'Camiseta básica ultra suave fabricada con algodón 100% orgánico certificado y libre de químicos.', 8.00, 19.99, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=600&auto=format&fit=crop', 100, 20, 'Levis', 'Original Tee', 'Blanco', 'M', NULL, 'activo');
