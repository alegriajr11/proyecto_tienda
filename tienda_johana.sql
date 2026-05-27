-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.1.0 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para tiendajohana_db
DROP DATABASE IF EXISTS `tiendajohana_db`;
CREATE DATABASE IF NOT EXISTS `tiendajohana_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tiendajohana_db`;

-- Volcando estructura para tabla tiendajohana_db.carrito
DROP TABLE IF EXISTS `carrito`;
CREATE TABLE IF NOT EXISTS `carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `cantidad` int DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_usuario_producto` (`usuario_id`,`producto_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.carrito: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.categorias
DROP TABLE IF EXISTS `categorias`;
CREATE TABLE IF NOT EXISTS `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.categorias: ~3 rows (aproximadamente)
INSERT IGNORE INTO `categorias` (`id`, `nombre`, `descripcion`, `created_at`) VALUES
	(1, 'Ropa', 'Prendas de vestir exclusivas, abrigos, camisetas y moda de última tendencia.', '2026-05-23 01:50:57'),
	(2, 'Calzado', 'Zapatos, tenis deportivos, botas y calzado artesanal premium.', '2026-05-23 01:50:57'),
	(3, 'Accesorios', 'Bolsos, relojes inteligentes, auriculares y complementos exclusivos.', '2026-05-23 01:50:57');

-- Volcando estructura para tabla tiendajohana_db.cupones
DROP TABLE IF EXISTS `cupones`;
CREATE TABLE IF NOT EXISTS `cupones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) NOT NULL,
  `descripcion` text,
  `tipo_descuento` enum('porcentaje','fijo') NOT NULL,
  `valor_descuento` decimal(10,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `usos_maximos` int DEFAULT '0',
  `usos_actuales` int DEFAULT '0',
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.cupones: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.direcciones
DROP TABLE IF EXISTS `direcciones`;
CREATE TABLE IF NOT EXISTS `direcciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `direccion` varchar(255) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `estado` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(20) DEFAULT NULL,
  `pais` varchar(100) NOT NULL,
  `tipo` enum('facturacion','envio') DEFAULT 'envio',
  `principal` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `direcciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.direcciones: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.inventario_movimientos
DROP TABLE IF EXISTS `inventario_movimientos`;
CREATE TABLE IF NOT EXISTS `inventario_movimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int DEFAULT NULL,
  `tipo` enum('entrada','salida') NOT NULL,
  `cantidad` int NOT NULL,
  `motivo` varchar(100) DEFAULT NULL,
  `referencia_tipo` enum('compra','venta','ajuste','devolucion') DEFAULT NULL,
  `referencia_id` int DEFAULT NULL,
  `fecha_movimiento` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `inventario_movimientos_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.inventario_movimientos: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.lista_deseos
DROP TABLE IF EXISTS `lista_deseos`;
CREATE TABLE IF NOT EXISTS `lista_deseos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `fecha_agregado` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_usuario_producto_deseos` (`usuario_id`,`producto_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `lista_deseos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `lista_deseos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.lista_deseos: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.pagos
DROP TABLE IF EXISTS `pagos`;
CREATE TABLE IF NOT EXISTS `pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int DEFAULT NULL,
  `monto` decimal(10,2) NOT NULL,
  `metodo_pago` enum('tarjeta_credito','tarjeta_debito','transferencia','efectivo','paypal') NOT NULL,
  `estado` enum('pendiente','completado','fallido','reembolsado') DEFAULT 'pendiente',
  `transaction_id` varchar(100) DEFAULT NULL,
  `fecha_pago` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.pagos: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.pedidos
DROP TABLE IF EXISTS `pedidos`;
CREATE TABLE IF NOT EXISTS `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `numero_pedido` varchar(50) NOT NULL,
  `estado` enum('pendiente','procesando','enviado','entregado','cancelado') DEFAULT 'pendiente',
  `subtotal` decimal(10,2) NOT NULL,
  `impuestos` decimal(10,2) DEFAULT '0.00',
  `gastos_envio` decimal(10,2) DEFAULT '0.00',
  `total` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  `direccion_envio_id` int DEFAULT NULL,
  `direccion_facturacion_id` int DEFAULT NULL,
  `fecha_pedido` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_envio` timestamp NULL DEFAULT NULL,
  `fecha_entrega` timestamp NULL DEFAULT NULL,
  `notas` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_pedido` (`numero_pedido`),
  KEY `usuario_id` (`usuario_id`),
  KEY `direccion_envio_id` (`direccion_envio_id`),
  KEY `direccion_facturacion_id` (`direccion_facturacion_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`direccion_envio_id`) REFERENCES `direcciones` (`id`) ON DELETE SET NULL,
  CONSTRAINT `pedidos_ibfk_3` FOREIGN KEY (`direccion_facturacion_id`) REFERENCES `direcciones` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.pedidos: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.pedido_detalles
DROP TABLE IF EXISTS `pedido_detalles`;
CREATE TABLE IF NOT EXISTS `pedido_detalles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `pedido_detalles_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pedido_detalles_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.pedido_detalles: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.productos
DROP TABLE IF EXISTS `productos`;
CREATE TABLE IF NOT EXISTS `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `categoria_id` int DEFAULT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `precio_compra` decimal(10,2) DEFAULT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `imagen` text,
  `stock_actual` int DEFAULT '0',
  `stock_minimo` int DEFAULT '0',
  `marca` varchar(50) DEFAULT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `color` varchar(30) DEFAULT NULL,
  `talla` varchar(20) DEFAULT NULL,
  `garantia_dias` int DEFAULT NULL,
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.productos: ~6 rows (aproximadamente)
INSERT IGNORE INTO `productos` (`id`, `categoria_id`, `nombre`, `descripcion`, `precio_compra`, `precio_venta`, `imagen`, `stock_actual`, `stock_minimo`, `marca`, `modelo`, `color`, `talla`, `garantia_dias`, `estado`, `created_at`, `updated_at`) VALUES
	(1, 1, 'Chaqueta de Cuero Premium', 'Chaqueta de cuero sintético estilo Biker de corte moderno, resistente al viento y muy elegante.', 45.00, 89.99, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?q=80&w=600&auto=format&fit=crop', 40, 8, 'Zara', 'Biker Classic', 'Negro', 'L', NULL, 'activo', '2026-05-23 01:50:57', '2026-05-23 01:50:57'),
	(2, 1, 'Camiseta de Algodón Orgánico', 'Camiseta básica ultra suave fabricada con algodón 100% orgánico certificado y libre de químicos.', 8.00, 19.99, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=600&auto=format&fit=crop', 100, 20, 'Levis', 'Original Tee', 'Blanco', 'M', NULL, 'activo', '2026-05-23 01:50:57', '2026-05-23 01:50:57'),
	(3, 2, 'Tenis Deportivos Urbanos', 'Tenis ergonómicos con amortiguación premium, perfectos para correr o uso casual de diario.', 60.00, 129.99, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=600&auto=format&fit=crop', 25, 4, 'Nike', 'Air Max 90', 'Rojo', '42', NULL, 'activo', '2026-05-23 01:50:57', '2026-05-23 01:50:57'),
	(4, 2, 'Botas de Cuero de Montaña', 'Botas impermeables fabricadas con cuero de alta densidad y suela antideslizante para todo terreno.', 90.00, 189.99, 'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?q=80&w=600&auto=format&fit=crop', 15, 3, 'Timberland', 'Classic Boots', 'Ocre', '41', NULL, 'activo', '2026-05-23 01:50:57', '2026-05-23 01:50:57'),
	(5, 3, 'Auriculares Inalámbricos Pro', 'Auriculares inteligentes de diadema con cancelación de ruido activa premium y sonido de alta fidelidad.', 150.00, 299.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=600&auto=format&fit=crop', 30, 6, 'Sony', 'WH-1000XM4', 'Negro', NULL, 180, 'activo', '2026-05-23 01:50:57', '2026-05-23 01:50:57'),
	(6, 3, 'Reloj Inteligente Elegante', 'Reloj inteligente premium con sensor de salud activo, pantalla retina y correa de silicona deportiva.', 200.00, 399.99, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=600&auto=format&fit=crop', 6, 5, 'Apple', 'Series 9 Pro', 'Negro', 'None', 365, 'activo', '2026-05-23 01:50:57', '2026-05-23 04:01:50');

-- Volcando estructura para tabla tiendajohana_db.reseñas
DROP TABLE IF EXISTS `reseñas`;
CREATE TABLE IF NOT EXISTS `reseñas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  `calificacion` int DEFAULT NULL,
  `comentario` text,
  `fecha_resena` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_usuario_producto_resena` (`usuario_id`,`producto_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `reseñas_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reseñas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reseñas_chk_1` CHECK (((`calificacion` >= 1) and (`calificacion` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.reseñas: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tiendajohana_db.slides
DROP TABLE IF EXISTS `slides`;
CREATE TABLE IF NOT EXISTS `slides` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `subtitulo` varchar(200) DEFAULT NULL,
  `imagen_url` text NOT NULL,
  `texto_boton` varchar(100) DEFAULT 'Ver Catálogo',
  `enlace_boton` varchar(255) DEFAULT '/',
  `posicion_texto` enum('izquierda','derecha','centro') DEFAULT 'izquierda',
  `orden` int DEFAULT '0',
  `activo` tinyint(1) DEFAULT '1',
  `creado_por` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `creado_por` (`creado_por`),
  CONSTRAINT `slides_ibfk_1` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.slides: ~2 rows (aproximadamente)
INSERT IGNORE INTO `slides` (`id`, `titulo`, `subtitulo`, `imagen_url`, `texto_boton`, `enlace_boton`, `posicion_texto`, `orden`, `activo`, `creado_por`, `created_at`, `updated_at`) VALUES
	(3, 'Nueva Colección Primavera 2026', 'Moda Exclusiva', 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600&q=80', 'Ver Colección', '/ropa', 'izquierda', 1, 1, NULL, '2026-05-25 04:03:21', '2026-05-25 04:03:21'),
	(4, 'Accesorios que Definen tu Estilo', 'Complementos Premium', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1600&q=80', 'Ver Accesorios', '/accesorios', 'izquierda', 2, 1, NULL, '2026-05-25 04:03:21', '2026-05-25 04:07:38');

-- Volcando estructura para tabla tiendajohana_db.usuarios
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` enum('cliente','administrador','empleado') DEFAULT 'cliente',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ultimo_acceso` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla tiendajohana_db.usuarios: ~0 rows (aproximadamente)
INSERT IGNORE INTO `usuarios` (`id`, `nombre`, `apellido`, `correo`, `telefono`, `contrasena`, `rol`, `fecha_registro`, `ultimo_acceso`) VALUES
	(1, 'Administrador', 'TiendaPOO', 'admin@tiendapoo.com', '', 'scrypt:32768:8:1$AP4XYUtefwXwIHUt$96463c6fdd552cc2ac6e15b4ad819878e6db81dfac7e13f81884d3090fc720b9f202a90b188eee38cfe96cd409696c73451ca075a3b0eb670bc7eb109c59e1d2', 'administrador', '2026-05-23 03:57:17', NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
