from models.database import Database
from models.interfaces import ICarritoRepository
from models.exceptions import RepositoryError

class CarritoRepository(ICarritoRepository):
    """
    Repositorio de persistencia para el Carrito de compras.
    Implementa ICarritoRepository para seguir ISP y DIP.
    """
    def __init__(self):
        self.db = Database()

    def agregar_producto(self, usuario_id, producto_id, cantidad=1):
        try:
            conn = self.db.connect()
            if not conn: return False
                
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO carrito (usuario_id, producto_id, cantidad) 
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE cantidad = cantidad + %s
                """
                cursor.execute(query, (usuario_id, producto_id, cantidad, cantidad))
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                raise RepositoryError(f"Error al agregar al carrito: {str(e)}")
            finally:
                conn.close()
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def obtener_carrito(self, usuario_id):
        try:
            conn = self.db.connect()
            items = []
            if not conn: return items
                
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT c.id AS carrito_item_id, c.producto_id, c.cantidad, 
                           p.nombre, p.precio_venta, p.imagen, p.descripcion
                    FROM carrito c
                    INNER JOIN productos p ON c.producto_id = p.id
                    WHERE c.usuario_id = %s
                """
                cursor.execute(query, (usuario_id,))
                items = cursor.fetchall()
                cursor.close()
            except Exception as e:
                raise RepositoryError(f"Error al obtener carrito: {str(e)}")
            finally:
                conn.close()
            return items
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def eliminar_producto(self, usuario_id, producto_id):
        try:
            conn = self.db.connect()
            if not conn: return False
                
            try:
                cursor = conn.cursor()
                query = "DELETE FROM carrito WHERE usuario_id = %s AND producto_id = %s"
                cursor.execute(query, (usuario_id, producto_id))
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                raise RepositoryError(f"Error al eliminar del carrito: {str(e)}")
            finally:
                conn.close()
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def vaciar_carrito(self, usuario_id):
        try:
            conn = self.db.connect()
            if not conn: return False
                
            try:
                cursor = conn.cursor()
                query = "DELETE FROM carrito WHERE usuario_id = %s"
                cursor.execute(query, (usuario_id,))
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                raise RepositoryError(f"Error al vaciar carrito: {str(e)}")
            finally:
                conn.close()
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def obtener_cantidad_total(self, usuario_id):
        try:
            conn = self.db.connect()
            if not conn: return 0
                
            try:
                cursor = conn.cursor()
                query = "SELECT SUM(cantidad) FROM carrito WHERE usuario_id = %s"
                cursor.execute(query, (usuario_id,))
                result = cursor.fetchone()
                cursor.close()
                
                if result and result[0] is not None:
                    return int(result[0])
                return 0
            except Exception as e:
                raise RepositoryError(f"Error al obtener total del carrito: {str(e)}")
            finally:
                conn.close()
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")
