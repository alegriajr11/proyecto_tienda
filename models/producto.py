class Producto:
    """
    Clase base para todos los productos de la tienda.
    Demuestra Encapsulamiento (atributos protegidos/privados).
    """
    def __init__(self, id, nombre, precio, descripcion, imagen):
        self._id = id             # El guion bajo indica que es un atributo "protegido"
        self._nombre = nombre
        self._precio = precio
        self._descripcion = descripcion
        self._imagen = imagen

    # Getters (Propiedades) para acceder a los atributos encapsulados
    @property
    def id(self): return self._id
    
    @property
    def nombre(self): return self._nombre
    
    @property
    def precio(self): return self._precio
    
    @property
    def descripcion(self): return self._descripcion
    
    @property
    def imagen(self): return self._imagen

    def mostrar_info(self):
        """Método que será sobrescrito (Polimorfismo) en clases hijas."""
        return f"Producto: {self._nombre} - ${self._precio}"

class Electronico(Producto):
    """
    Clase que HEREDA de Producto. Representa productos tecnológicos.
    """
    def __init__(self, id, nombre, precio, descripcion, imagen, garantia):
        # Llamamos al constructor de la clase Padre (Producto)
        super().__init__(id, nombre, precio, descripcion, imagen)
        self._garantia = garantia
        
    @property
    def garantia(self): return self._garantia

    def mostrar_info(self):
        """POLIMORFISMO: Comportamiento específico para Electrónicos"""
        return f"[Electrónico] {self._nombre} - Garantía: {self._garantia}"

class Ropa(Producto):
    """
    Clase que HEREDA de Producto. Representa prendas de vestir.
    """
    def __init__(self, id, nombre, precio, descripcion, imagen, talla):
        super().__init__(id, nombre, precio, descripcion, imagen)
        self._talla = talla
        
    @property
    def talla(self): return self._talla

    def mostrar_info(self):
        """POLIMORFISMO: Comportamiento específico para Ropa"""
        return f"[Ropa] {self._nombre} - Talla: {self._talla}"
