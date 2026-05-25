# Script de migración para crear la tabla de slides y agregar datos iniciales.
# Ejecutar una sola vez: python migrar_slides.py

from models.database import Database

db = Database()
conn = db.connect()

if conn:
    try:
        cursor = conn.cursor()
        
        # Crear tabla de slides
        cursor.execute("""
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
            )
        """)
        
        # Insertar slides iniciales (los que ya estaban estáticos)
        cursor.execute("SELECT COUNT(*) FROM slides")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("""
                INSERT INTO slides (titulo, subtitulo, imagen_url, texto_boton, enlace_boton, posicion_texto, orden, activo) VALUES
                ('Nueva Colección Primavera 2026', 'Moda Exclusiva', 
                 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600&q=80',
                 'Ver Colección', '/ropa', 'izquierda', 1, TRUE),
                ('Accesorios que Definen tu Estilo', 'Complementos Premium',
                 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1600&q=80',
                 'Ver Accesorios', '/accesorios', 'derecha', 2, TRUE)
            """)
            print("Slides iniciales insertados correctamente.")
        else:
            print(f"Ya existen {count} slides en la base de datos.")
        
        conn.commit()
        cursor.close()
        print("Tabla 'slides' creada/verificada exitosamente.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print("No se pudo conectar a la base de datos.")
