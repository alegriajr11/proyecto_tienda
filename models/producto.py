class Producto:
    """
    Clase base para todos los productos de la tienda.
    Demuestra Encapsulamiento (atributos protegidos/privados).
    """
    def __init__(self, id, nombre, precio_venta, descripcion, imagen, stock_actual=0, stock_minimo=0, marca=None, modelo=None, color=None, precio_compra=0):
        self._id = id             # El guion bajo indica que es un atributo "protegido"
        self._nombre = nombre
        self._precio_venta = precio_venta
        self._descripcion = descripcion
        self._imagen = imagen
        self._stock_actual = stock_actual
        self._stock_minimo = stock_minimo
        self._marca = marca
        self._modelo = modelo
        self._color = color
        self._precio_compra = precio_compra

    # Getters (Propiedades) para acceder a los atributos encapsulados
    @property
    def id(self): return self._id
    
    @property
    def nombre(self): return self._nombre
    
    @property
    def precio_venta(self): return self._precio_venta
    
    @property
    def descripcion(self): return self._descripcion
    
    @property
    def imagen(self): return self._imagen

    @property
    def stock_actual(self): return self._stock_actual

    @property
    def stock_minimo(self): return self._stock_minimo

    @property
    def marca(self): return self._marca

    @property
    def modelo(self): return self._modelo

    @property
    def color(self): return self._color

    @property
    def precio_compra(self): return self._precio_compra

    def mostrar_info(self):
        """Método que será sobrescrito (Polimorfismo) en clases hijas."""
        return f"Producto: {self._nombre} - ${self._precio_venta}"

class Electronico(Producto):
    """
    Clase que HEREDA de Producto. Representa productos tecnológicos.
    """
    def __init__(self, id, nombre, precio_venta, descripcion, imagen, garantia_dias, stock_actual=0, stock_minimo=0, marca=None, modelo=None, color=None, precio_compra=0):
        # Llamamos al constructor de la clase Padre (Producto)
        super().__init__(id, nombre, precio_venta, descripcion, imagen, stock_actual, stock_minimo, marca, modelo, color, precio_compra)
        self._garantia_dias = garantia_dias
        
    @property
    def garantia_dias(self): return self._garantia_dias

    def mostrar_info(self):
        """POLIMORFISMO: Comportamiento específico para Electrónicos"""
        garantia_str = f"{self._garantia_dias} días" if self._garantia_dias else "Sin garantía especificada"
        return f"[Electrónico] {self._nombre} - Garantía: {garantia_str}"

class Ropa(Producto):
    """
    Clase que HEREDA de Producto. Representa prendas de vestir.
    """
    def __init__(self, id, nombre, precio_venta, descripcion, imagen, talla, stock_actual=0, stock_minimo=0, marca=None, modelo=None, color=None, precio_compra=0):
        super().__init__(id, nombre, precio_venta, descripcion, imagen, stock_actual, stock_minimo, marca, modelo, color, precio_compra)
        self._talla = talla
        
    @property
    def talla(self): return self._talla

    def mostrar_info(self):
        """POLIMORFISMO: Comportamiento específico para Ropa"""
        talla_str = self._talla if self._talla else "Estándar"
        return f"[Ropa] {self._nombre} - Talla: {talla_str}"
