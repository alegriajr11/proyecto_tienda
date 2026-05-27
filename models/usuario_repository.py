from models.database import Database
from models.usuario import Usuario
from models.interfaces import IUsuarioRepository
from models.exceptions import RepositoryError, AuthenticationError, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioRepository(IUsuarioRepository):
    """
    Repositorio de persistencia y operaciones de seguridad para la entidad Usuario.
    Implementa IUsuarioRepository para seguir DIP.
    """
    def __init__(self):
        self.db = Database()

    def crear_usuario(self, nombre, apellido, correo, telefono, contrasena_plana):
        try:
            conn = self.db.connect()
            if not conn: return False
                
            try:
                cursor = conn.cursor()
                contrasena_cifrada = generate_password_hash(contrasena_plana)
                query = """
                    INSERT INTO usuarios (nombre, apellido, correo, telefono, contrasena) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, apellido, correo, telefono, contrasena_cifrada))
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                raise RepositoryError(f"Error al crear usuario: {str(e)}")
            finally:
                conn.close()
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def buscar_por_correo(self, correo):
        try:
            conn = self.db.connect()
            usuario = None
            if not conn: return None
                
            try:
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM usuarios WHERE correo = %s"
                cursor.execute(query, (correo,))
                fila = cursor.fetchone()
                
                if fila:
                    usuario = Usuario(
                        id=fila['id'], 
                        nombre=fila['nombre'], 
                        correo=fila['correo'], 
                        contrasena=fila['contrasena'],
                        rol=fila.get('rol', 'cliente')
                    )
                cursor.close()
            except Exception as e:
                raise RepositoryError(f"Error al buscar usuario: {str(e)}")
            finally:
                conn.close()
            return usuario
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def obtener_por_id(self, usuario_id):
        try:
            conn = self.db.connect()
            usuario = None
            if not conn: return None
                
            try:
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM usuarios WHERE id = %s"
                cursor.execute(query, (usuario_id,))
                fila = cursor.fetchone()
                
                if fila:
                    usuario = Usuario(
                        id=fila['id'], 
                        nombre=fila['nombre'], 
                        correo=fila['correo'], 
                        contrasena=fila['contrasena'],
                        rol=fila.get('rol', 'cliente')
                    )
                cursor.close()
            except Exception as e:
                raise RepositoryError(f"Error al obtener usuario por ID: {str(e)}")
            finally:
                conn.close()
            return usuario
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def verificar_contrasena(self, correo, contrasena_plana):
        usuario_db = self.buscar_por_correo(correo)
        if not usuario_db: 
            raise AuthenticationError("El correo electrónico no está registrado")
            
        if check_password_hash(usuario_db._contrasena, contrasena_plana):
            return usuario_db
        
        raise AuthenticationError("Contraseña incorrecta")
