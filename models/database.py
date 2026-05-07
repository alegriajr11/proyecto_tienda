import mysql.connector
from mysql.connector import Error

class Database:
    """
    Clase que gestiona la conexión a la base de datos MySQL.
    Aplica el principio de Responsabilidad Única (SRP).
    """
    def __init__(self):
        # NOTA PARA EL ESTUDIANTE: Si usas XAMPP en Windows, normalmente la contraseña está en blanco ('').
        # Si usas MAMP en Mac, la contraseña suele ser 'root'.
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'root' 
        self.database = 'tiendajohana_db'

    def connect(self):
        """Intenta establecer la conexión y la devuelve."""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return None
