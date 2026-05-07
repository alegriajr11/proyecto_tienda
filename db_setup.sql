CREATE DATABASE IF NOT EXISTS tiendajohana_db;
USE tiendajohana_db;

-- Tabla de Productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    imagen VARCHAR(255),
    tipo VARCHAR(50) DEFAULT 'general',
    atributo_extra VARCHAR(50) -- Almacena información específica como talla o garantía
);

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL
);

-- Tabla de Carrito
CREATE TABLE IF NOT EXISTS carrito (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_producto INT,
    cantidad INT DEFAULT 1,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE
);

-- Insertar datos de prueba para que los estudiantes vean algo al iniciar
INSERT INTO productos (nombre, precio, descripcion, imagen, tipo, atributo_extra) VALUES 
('Laptop HP Core i5', 1200.50, 'Laptop ideal para estudiantes de programación, 8GB RAM, 256GB SSD.', 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=600&auto=format&fit=crop', 'electronico', '12 meses'),
('Camiseta Python', 25.00, 'Camiseta de algodón con logo de Python. Muy cómoda.', 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=600&auto=format&fit=crop', 'ropa', 'Talla M'),
('Monitor Dell 24"', 150.00, 'Monitor Full HD para extender tu espacio de trabajo.', 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?q=80&w=600&auto=format&fit=crop', 'electronico', '24 meses'),
('Taza de Café Programador', 15.00, 'Taza de cerámica que convierte café en código.', 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?q=80&w=600&auto=format&fit=crop', 'general', '');
