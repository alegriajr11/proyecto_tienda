from abc import ABC, abstractmethod

class IRepository(ABC):
    """Interfaz base para todos los repositorios (ISP)."""
    @abstractmethod
    def obtener_por_id(self, id):
        pass

class IProductoRepository(IRepository):
    """Interfaz específica para el repositorio de productos."""
    @abstractmethod
    def obtener_todos_activos(self):
        pass

class IUsuarioRepository(IRepository):
    """Interfaz específica para el repositorio de usuarios."""
    @abstractmethod
    def crear_usuario(self, nombre, apellido, correo, telefono, contrasena_plana):
        pass

    @abstractmethod
    def buscar_por_correo(self, correo):
        pass

    @abstractmethod
    def verificar_contrasena(self, correo, contrasena_plana):
        pass

class ICarritoRepository(ABC):
    """Interfaz específica para el carrito (Segregación de Interfaces)."""
    @abstractmethod
    def agregar_producto(self, usuario_id, producto_id, cantidad=1):
        pass

    @abstractmethod
    def obtener_carrito(self, usuario_id):
        pass

    @abstractmethod
    def eliminar_producto(self, usuario_id, producto_id):
        pass

    @abstractmethod
    def vaciar_carrito(self, usuario_id):
        pass

    @abstractmethod
    def obtener_cantidad_total(self, usuario_id):
        pass

class ISlideRepository(ABC):
    """Interfaz para el repositorio de slides."""
    @abstractmethod
    def obtener_activos(self):
        pass

    @abstractmethod
    def obtener_todos(self):
        pass

    @abstractmethod
    def obtener_por_id(self, slide_id):
        pass

    @abstractmethod
    def crear(self, datos, usuario_id=None):
        pass

    @abstractmethod
    def actualizar(self, slide_id, datos):
        pass

    @abstractmethod
    def eliminar(self, slide_id):
        pass
