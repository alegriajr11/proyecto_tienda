from models.producto import Ropa, Accesorio, Zapato

class ProductoFactory:
    """
    Factoría para la creación polimórfica de objetos derivados de Producto.
    Actualizada para reflejar las categorías de la tienda: Accesorios, Ropa y Zapatos.
    """
    @staticmethod
    def crear_producto(fila):
        categoria = (fila.get('categoria_nombre') or '').lower().strip()
        
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
        
        if 'ropa' in categoria:
            return Ropa(
                talla=fila.get('talla', 'M'),
                **comunes
            )
        elif 'calzado' in categoria or 'zapato' in categoria:
            return Zapato(
                talla=fila.get('talla', '42'),
                **comunes
            )
        elif 'accesorios' in categoria:
            return Accesorio(
                material=fila.get('material', 'Cuero'),
                **comunes
            )
        else:
            # Por defecto, si no se reconoce, devolvemos un Accesorio general
            # Ya que Producto es abstracta y no se puede instanciar.
            return Accesorio(
                **comunes
            )
