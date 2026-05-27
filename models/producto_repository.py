from models.database import Database
from models.producto_factory import ProductoFactory
from models.interfaces import IProductoRepository
from models.exceptions import RepositoryError, EntityNotFoundError

class ProductoRepository(IProductoRepository):
    """
    Repositorio de persistencia y consultas para la entidad Producto.
    Implementa IProductoRepository para seguir DIP.
    """
    def __init__(self):
        # Database() ahora devuelve la misma instancia (Singleton)
        self.db = Database()

    def obtener_todos_activos(self):
        try:
            conn = self.db.connect()
            productos = []
            
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    query = """
                        SELECT p.*, c.nombre AS categoria_nombre 
                        FROM productos p 
                        LEFT JOIN categorias c ON p.categoria_id = c.id
                        WHERE p.estado = 'activo'
                    """
                    cursor.execute(query)
                    filas = cursor.fetchall()
                    
                    for fila in filas:
                        producto_objeto = ProductoFactory.crear_producto(fila)
                        productos.append(producto_objeto)
                        
                    cursor.close()
                except Exception as e:
                    raise RepositoryError(f"Error al obtener productos: {str(e)}")
                finally:
                    conn.close()
                    
            return productos
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def obtener_por_id(self, producto_id):
        try:
            conn = self.db.connect()
            producto = None
            
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    query = """
                        SELECT p.*, c.nombre AS categoria_nombre 
                        FROM productos p 
                        LEFT JOIN categorias c ON p.categoria_id = c.id
                        WHERE p.id = %s
                    """
                    cursor.execute(query, (producto_id,))
                    fila = cursor.fetchone()
                    
                    if fila:
                        producto = ProductoFactory.crear_producto(fila)
                    else:
                        raise EntityNotFoundError("Producto", producto_id)
                        
                    cursor.close()
                except EntityNotFoundError:
                    raise
                except Exception as e:
                    raise RepositoryError(f"Error al obtener producto {producto_id}: {str(e)}")
                finally:
                    conn.close()
                    
            return producto
        except (RepositoryError, EntityNotFoundError):
            raise
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")
