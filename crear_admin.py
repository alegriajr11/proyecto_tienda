# Script para crear un usuario administrador en la base de datos.
# Ejecutar una sola vez: python crear_admin.py
#
# Credenciales por defecto:
#   Correo: admin@tiendapoo.com
#   Contraseña: admin123

from models.database import Database
from werkzeug.security import generate_password_hash

db = Database()
conn = db.connect()

if conn:
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verificar si ya existe un admin
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", ('admin@tiendapoo.com',))
        existente = cursor.fetchone()
        
        if existente:
            print("El usuario administrador ya existe.")
        else:
            contrasena_cifrada = generate_password_hash('admin123')
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, correo, telefono, contrasena, rol) VALUES (%s, %s, %s, %s, %s, %s)",
                ('Administrador', 'TiendaPOO', 'admin@tiendapoo.com', '', contrasena_cifrada, 'administrador')
            )
            conn.commit()
            print("Usuario administrador creado exitosamente.")
            print("  Correo: admin@tiendapoo.com")
            print("  Contraseña: admin123")
        
        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print("No se pudo conectar a la base de datos.")
