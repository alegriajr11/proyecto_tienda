import mysql.connector
from mysql.connector import Error
from models.exceptions import DatabaseError

class Database:
    """
    Clase que gestiona la conexión a la base de datos MySQL.
    Aplica el patrón Singleton para asegurar una única instancia de conexión.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            # Inicialización de la configuración una sola vez
            cls._instance.host = 'localhost'
            cls._instance.user = 'root'
            cls._instance.password = 'root' 
            cls._instance.database = 'tiendajohana_db'
        return cls._instance

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
            # En lugar de solo imprimir, lanzamos nuestra excepción personalizada
            raise DatabaseError(f"Error al conectar con MySQL: {str(e)}")
