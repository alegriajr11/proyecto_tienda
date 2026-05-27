from abc import ABC, abstractmethod

# --- PATRÓN STRATEGY PARA DESCUENTOS ---

class EstrategiaDescuento(ABC):
    """Interfaz para las estrategias de descuento."""
    @abstractmethod
    def aplicar(self, precio):
        pass

class SinDescuento(EstrategiaDescuento):
    def aplicar(self, precio):
        return precio

class DescuentoPorcentaje(EstrategiaDescuento):
    def __init__(self, porcentaje):
        self.porcentaje = porcentaje
    
    def aplicar(self, precio):
        return precio * (1 - self.porcentaje / 100)

# --- CLASES DE PRODUCTO ---

class Producto(ABC):
    """
    Clase base ABSTRACTA para todos los productos de la tienda.
    Aplica OCP (Open/Closed Principle) al permitir nuevas categorías sin cambiar el código base.
    """
    def __init__(self, id, nombre, precio_venta, descripcion, imagen, stock_actual=0, stock_minimo=0, marca=None, modelo=None, color=None, precio_compra=0):
        self._id = id
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
        self._estrategia_descuento = SinDescuento() # Por defecto sin descuento

    @property
    def id(self): return self._id
    
    @property
    def nombre(self): return self._nombre
    
    @property
    def precio_venta(self): 
        # Aplicamos la estrategia de descuento al obtener el precio
        return self._estrategia_descuento.aplicar(self._precio_venta)
    
    @property
    def precio_base(self):
        return self._precio_venta

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

    def establecer_descuento(self, estrategia: EstrategiaDescuento):
        """Permite cambiar la estrategia de descuento dinámicamente (Strategy Pattern)."""
        self._estrategia_descuento = estrategia

    @abstractmethod
    def mostrar_info(self):
        """Método abstracto que obliga a las clases hijas a implementarlo."""
        pass

class Accesorio(Producto):
    """
    Clase para accesorios (reemplaza a Electronico para coherencia).
    """
    def __init__(self, id, nombre, precio_venta, descripcion, imagen, material=None, **kwargs):
        super().__init__(id, nombre, precio_venta, descripcion, imagen, **kwargs)
        self._material = material
        
    @property
    def material(self): return self._material

    def mostrar_info(self):
        material_str = f"Material: {self._material}" if self._material else "Accesorio general"
        return f"[Accesorio] {self._nombre} - {material_str}"

class Ropa(Producto):
    """
    Clase para prendas de vestir.
    """
    def __init__(self, id, nombre, precio_venta, descripcion, imagen, talla, **kwargs):
        super().__init__(id, nombre, precio_venta, descripcion, imagen, **kwargs)
        self._talla = talla
        
    @property
    def talla(self): return self._talla

    def mostrar_info(self):
        talla_str = self._talla if self._talla else "Estándar"
        return f"[Ropa] {self._nombre} - Talla: {talla_str}"

class Zapato(Ropa):
    """
    Clase específica para calzado, hereda de Ropa por la talla pero puede tener lógica propia.
    """
    def mostrar_info(self):
        return f"[Calzado] {self._nombre} - Talla: {self._talla}"
