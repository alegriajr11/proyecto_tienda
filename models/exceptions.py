class TiendaError(Exception):
    """Clase base para todas las excepciones de la tienda."""
    def __init__(self, mensaje="Ha ocurrido un error en la tienda"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class DatabaseError(TiendaError):
    """Excepción lanzada cuando hay problemas con la base de datos."""
    def __init__(self, mensaje="Error de conexión o consulta en la base de datos"):
        super().__init__(mensaje)

class RepositoryError(TiendaError):
    """Excepción base para errores en la capa de persistencia."""
    pass

class EntityNotFoundError(RepositoryError):
    """Lanzada cuando no se encuentra una entidad (Producto, Usuario, etc.)."""
    def __init__(self, entidad, id_entidad):
        self.mensaje = f"No se encontró la entidad {entidad} con ID: {id_entidad}"
        super().__init__(self.mensaje)

class AuthenticationError(TiendaError):
    """Lanzada cuando fallan las credenciales o el acceso."""
    def __init__(self, mensaje="Credenciales de acceso inválidas"):
        super().__init__(mensaje)

class ValidationError(TiendaError):
    """Lanzada cuando los datos de entrada no cumplen con las reglas de negocio."""
    pass

class StockError(TiendaError):
    """Lanzada cuando hay problemas con el inventario (ej. stock insuficiente)."""
    def __init__(self, producto_nombre):
        self.mensaje = f"Stock insuficiente para el producto: {producto_nombre}"
        super().__init__(self.mensaje)
