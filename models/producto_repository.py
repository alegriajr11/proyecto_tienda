# ¡Hola de nuevo! Aquí te presento el Repositorio de Productos (ProductoRepository).
#
# Principios SOLID aplicados aquí:
# 1. Single Responsibility Principle (SRP): Esta clase se encarga exclusivamente de las consultas
#    de base de datos MySQL relacionadas con los productos. El controlador ya no tiene código SQL
#    mezclado con la lógica de navegación.
# 2. Dependency Inversion Principle (DIP): Los controladores de Flask ahora dependen de este
#    repositorio para interactuar con los datos, aislando la lógica de base de datos de la lógica web.
#
# Adicionalmente, este repositorio delega la creación de objetos a 'ProductoFactory', lo que es una
# excelente combinación de patrones de diseño (Repository + Factory). ¡Así queda super profesional!

from models.database import Database
from models.producto_factory import ProductoFactory

class ProductoRepository:
    """
    Repositorio de persistencia y consultas para la entidad Producto.
    Aísla las consultas SQL de la capa de control.
    """
    def __init__(self):
        # Inyectamos la dependencia de Database (SRP)
        self.db = Database()

    def obtener_todos_activos(self):
        """
        Recupera todos los productos con estado 'activo' y mapea sus registros 
        a instancias del modelo correspondiente usando la Factoría.
        """
        conn = self.db.connect()
        productos = []
        
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                
                # Hacemos un JOIN con categorías para saber qué tipo de producto instanciar
                query = """
                    SELECT p.*, c.nombre AS categoria_nombre 
                    FROM productos p 
                    LEFT JOIN categorias c ON p.categoria_id = c.id
                    WHERE p.estado = 'activo'
                """
                cursor.execute(query)
                filas = cursor.fetchall()
                
                # Iteramos y transformamos los registros SQL crudos en objetos reales de Python
                for fila in filas:
                    producto_objeto = ProductoFactory.crear_producto(fila)
                    productos.append(producto_objeto)
                    
                cursor.close()
            except Exception as e:
                print(f"[ProductoRepository Error] No se pudieron obtener los productos: {e}")
            finally:
                conn.close()
                
        return productos

    def obtener_por_id(self, producto_id):
        """
        Busca un producto específico por su ID y lo devuelve instanciado como objeto.
        """
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
                    
                cursor.close()
            except Exception as e:
                print(f"[ProductoRepository Error] No se pudo obtener el producto con ID {producto_id}: {e}")
            finally:
                conn.close()
                
        return producto
