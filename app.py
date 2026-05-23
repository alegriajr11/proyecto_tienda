from flask import Flask
from controllers.main_controller import main
from controllers.admin_controller import admin

app = Flask(__name__)
# Usamos una clave secreta para poder utilizar sesiones y mensajes flash
app.secret_key = 'clave_secreta_de_johana'

# Registramos los controladores (Blueprints)
app.register_blueprint(main)
app.register_blueprint(admin)

if __name__ == '__main__':
    # El modo debug permite que la aplicación se reinicie automáticamente si hay cambios
    app.run(debug=True, port=5000)
