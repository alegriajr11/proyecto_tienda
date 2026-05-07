class Usuario:
    """
    Representa a un usuario del sistema.
    """
    def __init__(self, id, nombre, correo, contrasena):
        self._id = id
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena  # En un sistema real, esto debería estar encriptado

    @property
    def id(self): return self._id
    
    @property
    def nombre(self): return self._nombre
    
    @property
    def correo(self): return self._correo

    def saludar(self):
        return f"Hola, {self._nombre}!"
