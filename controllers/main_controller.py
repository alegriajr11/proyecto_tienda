from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import Database
from models.producto import Producto, Electronico, Ropa

# Creamos un Blueprint, que es una forma de organizar las rutas en Flask
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Ruta principal (Home). Muestra el catálogo de productos.
    """
    db = Database()
    conn = db.connect()
    productos = []
    
    if conn:
        # Usamos dictionary=True para poder acceder a las columnas por su nombre (ej: fila['nombre'])
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        
        for fila in filas:
            # Aquí aplicamos conceptos de POO (Instanciación de Clases Hijas)
            if fila['tipo'] == 'electronico':
                p = Electronico(fila['id'], fila['nombre'], fila['precio'], fila['descripcion'], fila['imagen'], fila['atributo_extra'])
            elif fila['tipo'] == 'ropa':
                p = Ropa(fila['id'], fila['nombre'], fila['precio'], fila['descripcion'], fila['imagen'], fila['atributo_extra'])
            else:
                p = Producto(fila['id'], fila['nombre'], fila['precio'], fila['descripcion'], fila['imagen'])
            
            productos.append(p)
            
        cursor.close()
        conn.close()
    
    # Pasamos la lista de objetos de Producto a la vista (index.html)
    return render_template('index.html', productos=productos)

@main.route('/contactos', methods=['GET', 'POST'])
def contacto():
    """
    Ruta para el formulario de contacto.
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        # En una aplicación real, aquí guardaríamos el mensaje o enviaríamos un email
        flash(f"¡Gracias por tu mensaje, {nombre}! Nos pondremos en contacto pronto.", "success")
        return redirect(url_for('main.contacto'))
    
    return render_template('contact.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta para inicio de sesión (Simulada para propósito educativo).
    """
    if request.method == 'POST':
        flash("Inicio de sesión exitoso (Simulado)", "success")
        return redirect(url_for('main.index'))
    return render_template('login.html')

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Ruta para registro de usuarios (Simulada).
    """
    if request.method == 'POST':
        flash("Usuario registrado exitosamente (Simulado)", "success")
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/carrito')
def carrito():
    """
    Ruta para ver el carrito de compras.
    (Actualmente es una vista estática, el estudiante puede implementar la lógica de base de datos)
    """
    return render_template('cart.html')
