import mysql.connector
from mysql.connector import Error

def init_db():
    print("Iniciando la configuración de la base de datos...")
    try:
        # Nos conectamos a MySQL sin especificar la base de datos inicialmente
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root' # Asegúrate que esta sea tu contraseña
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Leer el archivo SQL
            with open('db_setup.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
                
            # Ejecutar cada comando SQL separado por ';'
            # Ignoramos comandos vacíos
            commands = sql_script.split(';')
            
            for command in commands:
                if command.strip():
                    try:
                        cursor.execute(command)
                    except Error as ex:
                        print(f"Error ejecutando comando: {ex}")
            
            # Confirmar los cambios
            conn.commit()
            print("¡Base de datos y tablas creadas exitosamente!")
            
            cursor.close()
            conn.close()
            
    except Error as e:
        print(f"Error general de conexión: {e}")

if __name__ == '__main__':
    init_db()
