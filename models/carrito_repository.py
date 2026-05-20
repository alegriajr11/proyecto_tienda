# ¡Hola! Te presento el Repositorio del Carrito (CarritoRepository).
#
# ¿Por qué este repositorio es genial y respeta SOLID?
# 1. Single Responsibility Principle (SRP): Centraliza todas las consultas y modificaciones
#    de la tabla 'carrito' en la base de datos MySQL (agregar productos, obtener el listado,
#    eliminar unidades, vaciar el carrito).
# 2. Dependency Inversion Principle (DIP): Los controladores dependen de métodos sencillos como
#    'agregar_producto()' u 'obtener_carrito()' en lugar de escribir consultas JOIN complejas
#    directamente en las rutas. ¡Desacoplamiento total!

from models.database import Database

class CarritoRepository:
    """
    Repositorio de persistencia para el Carrito de compras.
    Maneja el almacenamiento y actualización de los productos seleccionados por cada usuario.
    """
    def __init__(self):
        # Inyección de dependencia (SRP)
        self.db = Database()

    def agregar_producto(self, usuario_id, producto_id, cantidad=1):
        """
        Agrega un producto al carrito de un usuario.
        Si el producto ya existe en su carrito, incrementa la cantidad (aprovechando la restricción UNIQUE).
        """
        conn = self.db.connect()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            
            # Usamos INSERT INTO ... ON DUPLICATE KEY UPDATE para que si el producto ya está en el carrito
            # de ese usuario, simplemente le sume la cantidad correspondiente. ¡Super eficiente!
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
            print(f"[CarritoRepository Error] No se pudo agregar el producto al carrito: {e}")
            return False
        finally:
            conn.close()

    def obtener_carrito(self, usuario_id):
        """
        Obtiene todos los ítems agregados al carrito de un usuario, con información detallada 
        del producto (nombre, precio_venta, imagen) mediante un INNER JOIN.
        """
        conn = self.db.connect()
        items = []
        if not conn:
            return items
            
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Hacemos una consulta con JOIN para traer el nombre del producto, el precio y la imagen
            # de cada elemento que está en el carrito del usuario.
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
            print(f"[CarritoRepository Error] Error al obtener el carrito del usuario {usuario_id}: {e}")
        finally:
            conn.close()
            
        return items

    def eliminar_producto(self, usuario_id, producto_id):
        """
        Elimina un producto del carrito de un usuario específico.
        """
        conn = self.db.connect()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            query = "DELETE FROM carrito WHERE usuario_id = %s AND producto_id = %s"
            cursor.execute(query, (usuario_id, producto_id))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"[CarritoRepository Error] No se pudo eliminar el producto del carrito: {e}")
            return False
        finally:
            conn.close()

    def vaciar_carrito(self, usuario_id):
        """
        Elimina todos los elementos del carrito de un usuario (por ejemplo, al finalizar la compra).
        """
        conn = self.db.connect()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            query = "DELETE FROM carrito WHERE usuario_id = %s"
            cursor.execute(query, (usuario_id,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"[CarritoRepository Error] No se pudo vaciar el carrito: {e}")
            return False
        finally:
            conn.close()

    def obtener_cantidad_total(self, usuario_id):
        """
        Retorna la cantidad total de artículos en el carrito del usuario.
        ¡Muy útil para el badge dinámico en el navbar! (SOLID - SRP)
        """
        conn = self.db.connect()
        if not conn:
            return 0
            
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
            print(f"[CarritoRepository Error] No se pudo obtener la cantidad total del carrito: {e}")
            return 0
        finally:
            conn.close()
