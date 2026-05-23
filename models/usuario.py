class Usuario:
    """
    Representa a un usuario del sistema.
    """
    def __init__(self, id, nombre, correo, contrasena, rol='cliente'):
        self._id = id
        self._nombre = nombre
        self._correo = correo
        self._contrasena = contrasena
        self._rol = rol

    @property
    def id(self): return self._id
    
    @property
    def nombre(self): return self._nombre
    
    @property
    def correo(self): return self._correo

    @property
    def rol(self): return self._rol

    def saludar(self):
        return f"Hola, {self._nombre}!"
