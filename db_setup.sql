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

-- Tabla de Slides del Banner Promocional
CREATE TABLE IF NOT EXISTS slides (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    subtitulo VARCHAR(200),
    imagen_url TEXT NOT NULL,
    texto_boton VARCHAR(100) DEFAULT 'Ver Catálogo',
    enlace_boton VARCHAR(255) DEFAULT '/',
    posicion_texto ENUM('izquierda', 'derecha', 'centro') DEFAULT 'izquierda',
    orden INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    creado_por INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (creado_por) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- =========================================================================
-- DATOS SEMILLA (Para pruebas de la tienda con la estructura profesional)
-- =========================================================================

-- Limpiar datos previos si existen (en orden inverso de dependencias)
DELETE FROM productos;
DELETE FROM categorias;

-- Insertar Categorías principales
INSERT INTO categorias (id, nombre, descripcion) VALUES
(1, 'Ropa', 'Prendas de vestir exclusivas, abrigos, camisetas y moda de última tendencia.'),
(2, 'Calzado', 'Zapatos, tenis deportivos, botas y calzado artesanal premium.'),
(3, 'Accesorios', 'Bolsos, relojes inteligentes, auriculares y complementos exclusivos.');

-- Insertar Productos semilla
INSERT INTO productos (nombre, categoria_id, descripcion, precio_compra, precio_venta, imagen, stock_actual, stock_minimo, marca, modelo, color, talla, garantia_dias, estado) VALUES
-- Ropa (ID: 1)
('Chaqueta de Cuero Premium', 1, 'Chaqueta de cuero sintético estilo Biker de corte moderno, resistente al viento y muy elegante.', 45.00, 89.99, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?q=80&w=600&auto=format&fit=crop', 40, 8, 'Zara', 'Biker Classic', 'Negro', 'L', NULL, 'activo'),
('Camiseta de Algodón Orgánico', 1, 'Camiseta básica ultra suave fabricada con algodón 100% orgánico certificado y libre de químicos.', 8.00, 19.99, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=600&auto=format&fit=crop', 100, 20, 'Levis', 'Original Tee', 'Blanco', 'M', NULL, 'activo'),
-- Calzado (ID: 2)
('Tenis Deportivos Urbanos', 2, 'Tenis ergonómicos con amortiguación premium, perfectos para correr o uso casual de diario.', 60.00, 129.99, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=600&auto=format&fit=crop', 25, 4, 'Nike', 'Air Max 90', 'Rojo', '42', NULL, 'activo'),
('Botas de Cuero de Montaña', 2, 'Botas impermeables fabricadas con cuero de alta densidad y suela antideslizante para todo terreno.', 90.00, 189.99, 'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?q=80&w=600&auto=format&fit=crop', 15, 3, 'Timberland', 'Classic Boots', 'Ocre', '41', NULL, 'activo'),
-- Accesorios (ID: 3)
('Auriculares Inalámbricos Pro', 3, 'Auriculares inteligentes de diadema con cancelación de ruido activa premium y sonido de alta fidelidad.', 150.00, 299.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=600&auto=format&fit=crop', 30, 6, 'Sony', 'WH-1000XM4', 'Negro', NULL, 180, 'activo'),
('Reloj Inteligente Elegante', 3, 'Reloj inteligente premium con sensor de salud activo, pantalla retina y correa de silicona deportiva.', 200.00, 399.99, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=600&auto=format&fit=crop', 20, 5, 'Apple', 'Series 9 Pro', 'Negro', NULL, 365, 'activo');

