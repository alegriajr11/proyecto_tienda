from flask import Flask
from controllers.main_controller import main

app = Flask(__name__)
# Usamos una clave secreta para poder utilizar sesiones y mensajes flash
app.secret_key = 'clave_secreta_de_johana'

# Registramos el controlador principal (Blueprint)
app.register_blueprint(main)

if __name__ == '__main__':
    # El modo debug permite que la aplicación se reinicie automáticamente si hay cambios
    app.run(debug=True, port=5000)
