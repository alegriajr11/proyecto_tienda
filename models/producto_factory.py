# ¡Hola! Soy el dev junior y he creado esta clase Factory (Factoría) para cumplir con los principios SOLID.
#
# ¿Por qué aplicamos SOLID aquí?
# 1. Single Responsibility Principle (SRP): Esta clase tiene una ÚNICA responsabilidad, que es decidir
#    e instanciar la clase correcta de Producto según la fila de la base de datos.
# 2. Open/Closed Principle (OCP): Si mañana creamos una nueva clase como "ServicioDigital" que herede
#    de Producto, solo tenemos que añadir un "elif" aquí. Los controladores y los repositorios no
#    necesitan cambiar en absoluto. ¡Es super escalable!

from models.producto import Producto, Electronico, Ropa

class ProductoFactory:
    """
    Factoría para la creación polimórfica de objetos derivados de Producto.
    Mapea las filas de la base de datos a sus clases correspondientes en Python.
    """
    @staticmethod
    def crear_producto(fila):
        # Obtenemos la categoría en minúsculas y sin espacios para evitar errores de escritura
        categoria = (fila.get('categoria_nombre') or '').lower().strip()
        
        # Parámetros comunes de la clase base
        comunes = {
            'id': fila['id'],
            'nombre': fila['nombre'],
            'precio_venta': fila['precio_venta'],
            'descripcion': fila['descripcion'],
            'imagen': fila['imagen'],
            'stock_actual': fila.get('stock_actual', 0),
            'stock_minimo': fila.get('stock_minimo', 0),
            'marca': fila.get('marca'),
            'modelo': fila.get('modelo'),
            'color': fila.get('color'),
            'precio_compra': fila.get('precio_compra', 0)
        }
        
        # Instanciamos la clase hija correcta según la categoría de la base de datos
        if 'electrónica' in categoria or 'electronica' in categoria:
            return Electronico(
                garantia_dias=fila.get('garantia_dias', 365),
                **comunes
            )
        elif 'ropa' in categoria:
            return Ropa(
                talla=fila.get('talla', 'M'),
                **comunes
            )
        else:
            # Si no es ninguna categoría especial, devolvemos un producto general
            return Producto(
                **comunes
            )
