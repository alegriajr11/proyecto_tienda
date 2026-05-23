# ¡Hola! Aquí te presento el Repositorio de Usuarios (UsuarioRepository).
#
# ¿Por qué este repositorio es genial y sigue SOLID?
# 1. Single Responsibility Principle (SRP): Esta clase se encarga ÚNICAMENTE de la persistencia de los
#    usuarios en la base de datos MySQL (crear, buscar, validar contraseñas). El controlador no tiene
#    que saber nada de cómo se guardan o se validan los usuarios.
# 2. Seguridad Incorporada (Buenas Prácticas): En lugar de guardar contraseñas en texto plano (¡lo cual
#    sería un grave error de seguridad!), usamos 'generate_password_hash' y 'check_password_hash'
#    de la librería 'werkzeug.security' de Flask para proteger la información de nuestros usuarios.

from models.database import Database
from models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioRepository:
    """
    Repositorio de persistencia y operaciones de seguridad para la entidad Usuario.
    Maneja el registro, búsqueda y autenticación de usuarios.
    """
    def __init__(self):
        # Inyección de dependencia (SRP)
        self.db = Database()

    def crear_usuario(self, nombre, apellido, correo, telefono, contrasena_plana):
        """
        Cifra la contraseña y registra un nuevo usuario en la base de datos.
        """
        conn = self.db.connect()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            
            # ¡Muy importante! Ciframos la contraseña usando un algoritmo de hashing seguro
            contrasena_cifrada = generate_password_hash(contrasena_plana)
            
            query = """
                INSERT INTO usuarios (nombre, apellido, correo, telefono, contrasena) 
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nombre, apellido, correo, telefono, contrasena_cifrada)
            cursor.execute(query, valores)
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"[UsuarioRepository Error] No se pudo registrar el usuario: {e}")
            return False
        finally:
            conn.close()

    def buscar_por_correo(self, correo):
        """
        Busca un usuario por su correo electrónico y devuelve un objeto Usuario o None.
        """
        conn = self.db.connect()
        usuario = None
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE correo = %s"
            cursor.execute(query, (correo,))
            fila = cursor.fetchone()
            
            if fila:
                # Instanciamos la entidad de negocio limpia Usuario (SRP)
                usuario = Usuario(
                    id=fila['id'], 
                    nombre=fila['nombre'], 
                    correo=fila['correo'], 
                    contrasena=fila['contrasena'],
                    rol=fila.get('rol', 'cliente')
                )
                
            cursor.close()
        except Exception as e:
            print(f"[UsuarioRepository Error] Error al buscar usuario por correo: {e}")
        finally:
            conn.close()
            
        return usuario

    def verificar_contrasena(self, correo, contrasena_plana):
        """
        Valida las credenciales de un usuario. Devolvemos el objeto Usuario si es correcto,
        o None si las credenciales son incorrectas.
        """
        # 1. Buscamos al usuario por su correo electrónico
        usuario_db = self.buscar_por_correo(correo)
        if not usuario_db:
            return None
            
        # 2. Comparamos la contraseña en texto plano con el hash seguro guardado en la base de datos
        # Nota: ¡Nunca comparamos texto plano directamente con el hash! check_password_hash hace el trabajo por nosotros.
        if check_password_hash(usuario_db._contrasena, contrasena_plana):
            return usuario_db
            
        return None
