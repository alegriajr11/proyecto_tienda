# ¡Hola! Soy el dev junior y he reescrito el controlador principal (main_controller.py)
# para que consuma la base de datos de manera REAL.
#
# Principios SOLID aplicados aquí de forma estricta:
# 1. Single Responsibility Principle (SRP): Las rutas solo manejan la petición HTTP, redirecciones
#    y renderizado de plantillas. No contienen consultas SQL crudas en absoluto. Delegamos toda la
#    lógica de base de datos a los repositorios correspondientes.
# 2. Dependency Inversion Principle (DIP): Inyectamos y consumimos los repositorios:
#    - 'producto_repo' para traer los productos activos.
#    - 'usuario_repo' para el registro y login real de usuarios con claves encriptadas.
#    - 'carrito_repo' para las acciones del carrito de compras.
#
# ¡Esto es super ordenado y escalable! Las rutas son super limpias.

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.producto_repository import ProductoRepository
from models.usuario_repository import UsuarioRepository
from models.carrito_repository import CarritoRepository

def login_required(f):
    """
    Decorador de seguridad para proteger rutas que requieren autenticación.
    ¡Super pro y aplicando DRY para evitar repetir validaciones de sesión!
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Por favor, inicia sesión para acceder a tu carrito de compras.", "warning")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function


# Creamos el Blueprint principal
main = Blueprint('main', __name__)

# Instanciamos los repositorios a nivel de módulo para reutilizarlos en cada ruta (SOLID - SRP)
producto_repo = ProductoRepository()
usuario_repo = UsuarioRepository()
carrito_repo = CarritoRepository()

@main.context_processor
def inject_cart_count():
    # ¡Un toque súper pro de un junior apasionado!
    # Obtenemos la cantidad total de artículos en el carrito de manera dinámica
    # para mostrar un hermoso badge en el navbar. (SOLID - SRP)
    cantidad_total = 0
    if 'usuario_id' in session:
        cantidad_total = carrito_repo.obtener_cantidad_total(session['usuario_id'])
    else:
        # Sumamos las cantidades de los productos en el carrito temporal de sesión
        carrito_sesion = session.get('carrito', {})
        cantidad_total = sum(int(cant) for cant in carrito_sesion.values())
    return dict(cart_count=cantidad_total)

@main.route('/')
def index():
    """
    Ruta principal (Catálogo). Filtra dinámicamente los productos por categoría.
    ¡Super pro, rápido y aplicando OOP al inspeccionar tipos polimórficos!
    """
    categoria_filtro = request.args.get('categoria')
    todos = producto_repo.obtener_todos_activos()
    
    # Variables para personalizar la vista por categoría
    titulo_seccion = None
    descripcion_seccion = None
    
    if categoria_filtro:
        filtro = categoria_filtro.lower().strip()
        productos = []
        for p in todos:
            clase = p.__class__.__name__.lower()
            if filtro == 'ropa' and clase == 'ropa':
                productos.append(p)
            elif (filtro == 'accesorios' or filtro == 'electronica') and clase == 'electronico':
                productos.append(p)
            elif filtro == 'calzado' and clase == 'ropa' and p.talla.isdigit():
                productos.append(p)
            elif filtro == 'general' and clase == 'producto':
                productos.append(p)
        
        # Títulos y descripciones personalizadas por categoría
        if filtro == 'ropa':
            titulo_seccion = "Moda y Ropa Exclusiva"
            descripcion_seccion = "Prendas de vestir exclusivas, abrigos, chaquetas y camisetas diseñadas con materiales premium."
        elif filtro == 'calzado':
            titulo_seccion = "Calzado y Zapatos Premium"
            descripcion_seccion = "Nuestra colección exclusiva de tenis deportivos, botas todoterreno y zapatos de cuero artesanal."
        elif filtro in ('accesorios', 'electronica'):
            titulo_seccion = "Accesorios y Gadgets Exclusivos"
            descripcion_seccion = "Relojes inteligentes, auriculares con cancelación de ruido y los mejores complementos para tu estilo."
            categoria_filtro = 'accesorios'
        elif filtro == 'ofertas':
            titulo_seccion = "Promociones y Ofertas Especiales"
            descripcion_seccion = "Aprovecha nuestros descuentos de hasta el 20% en prendas y artículos seleccionados por tiempo limitado."
        
        # Si el filtro no coincide con nada, mostramos todos por defecto
        if not productos:
            productos = todos
            categoria_filtro = None
    else:
        productos = todos
        
    return render_template(
        'index.html', 
        productos=productos, 
        categoria_activa=categoria_filtro,
        titulo_seccion=titulo_seccion,
        descripcion_seccion=descripcion_seccion
    )

@main.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    """
    Ruta para ver el detalle completo de un producto individual.
    """
    producto = producto_repo.obtener_por_id(producto_id)
    if not producto:
        flash("El producto solicitado no fue encontrado.", "danger")
        return redirect(url_for('main.index'))
    
    # Obtenemos productos relacionados (misma clase) para sugerencias
    todos = producto_repo.obtener_todos_activos()
    relacionados = [p for p in todos if p.__class__.__name__ == producto.__class__.__name__ and p.id != producto.id][:4]
    
    return render_template(
        'producto_detalle.html',
        producto=producto,
        relacionados=relacionados
    )

@main.route('/contactos', methods=['GET', 'POST'])
def contacto():
    """
    Ruta para el formulario de contacto.
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        flash(f"¡Gracias por tu mensaje, {nombre}! Nos pondremos en contacto pronto.", "success")
        return redirect(url_for('main.contacto'))
    
    return render_template('contact.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta para inicio de sesión real. Verifica contra la base de datos.
    """
    # Si ya inició sesión, lo mandamos al destino correcto según su rol
    if 'usuario_id' in session:
        if session.get('usuario_rol') == 'administrador':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        
        # Validamos usando nuestro repositorio de usuarios (SRP y seguridad encriptada)
        usuario = usuario_repo.verificar_contrasena(correo, contrasena)
        
        if usuario:
            # Iniciamos sesión real guardando datos en la sesión de Flask
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            session['usuario_rol'] = usuario.rol
            
            # ¡Fusión inteligente del carrito de sesión temporal con la base de datos!
            carrito_sesion = session.get('carrito', {})
            if carrito_sesion:
                for prod_id_str, cant in carrito_sesion.items():
                    carrito_repo.agregar_producto(usuario.id, int(prod_id_str), cantidad=cant)
                # Limpiamos el carrito temporal una vez fusionado en la base de datos
                session.pop('carrito', None)
                session.modified = True
                flash(f"¡Bienvenido de nuevo, {usuario.nombre}! Hemos recuperado e importado tus productos seleccionados.", "success")
            else:
                flash(f"¡Bienvenido de nuevo, {usuario.nombre}! Inicio de sesión exitoso.", "success")
            
            # Redirigir según el rol del usuario
            if usuario.rol == 'administrador':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))
        else:
            flash("Correo electrónico o contraseña incorrectos. Por favor, intenta de nuevo.", "danger")
            
    return render_template('login.html')

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Ruta para registro real de usuarios. Guarda de forma segura con contraseña encriptada.
    """
    if 'usuario_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        confirmar = request.form.get('confirmar')
        
        # Validaciones de seguridad en el controlador
        if contrasena != confirmar:
            flash("Las contraseñas ingresadas no coinciden.", "danger")
            return render_template('register.html')
            
        # Comprobamos si el correo ya está registrado en la base de datos
        usuario_existente = usuario_repo.buscar_por_correo(correo)
        if usuario_existente:
            flash("El correo electrónico ingresado ya se encuentra registrado.", "danger")
            return render_template('register.html')
            
        # Registramos al usuario en la base de datos usando el repositorio
        exito = usuario_repo.crear_usuario(
            nombre=nombre, 
            apellido='',  # Lo dejamos vacío por defecto, expandible en el futuro
            correo=correo, 
            telefono='', 
            contrasena_plana=contrasena
        )
        
        if exito:
            flash("¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('main.login'))
        else:
            flash("Ocurrió un error inesperado al crear la cuenta. Inténtalo de nuevo.", "danger")
            
    return render_template('register.html')

@main.route('/logout')
def logout():
    """
    Ruta para cerrar sesión. Limpia la sesión del usuario de Flask.
    """
    session.pop('usuario_id', None)
    session.pop('usuario_nombre', None)
    session.pop('usuario_rol', None)
    flash("Has cerrado tu sesión de forma segura.", "success")
    return redirect(url_for('main.index'))

@main.route('/carrito')
def carrito():
    """
    Ruta para ver el carrito de compras real o de sesión sin obligar a iniciar sesión.
    """
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        items = carrito_repo.obtener_carrito(usuario_id)
    else:
        # Carrito anónimo en sesión
        carrito_sesion = session.get('carrito', {})
        items = []
        for prod_id_str, cant in carrito_sesion.items():
            producto = producto_repo.obtener_por_id(int(prod_id_str))
            if producto:
                items.append({
                    'carrito_item_id': f"session_{prod_id_str}",
                    'producto_id': producto.id,
                    'cantidad': cant,
                    'nombre': producto.nombre,
                    'precio_venta': producto.precio_venta,
                    'imagen': producto.imagen,
                    'descripcion': producto.descripcion
                })
    
    # Realizamos los cálculos del total de forma dinámica y profesional
    subtotal = sum(float(item['precio_venta']) * int(item['cantidad']) for item in items)
    
    # Ofrecemos envío gratis a partir de $500.00
    gastos_envio = 15.00 if subtotal < 500.00 and subtotal > 0 else 0.00
    total = subtotal + gastos_envio
    
    # Pasamos las variables a la vista (cart.html)
    return render_template(
        'cart.html', 
        items=items, 
        subtotal=subtotal, 
        gastos_envio=gastos_envio, 
        total=total
    )

@main.route('/carrito/agregar/<int:producto_id>', methods=['POST', 'GET'])
def agregar_al_carrito(producto_id):
    """
    Agrega un producto al carrito de compras real (BD) o temporal (sesión).
    """
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        exito = carrito_repo.agregar_producto(usuario_id, producto_id, cantidad=1)
    else:
        # Carrito temporal en sesión para usuarios no registrados
        if 'carrito' not in session:
            session['carrito'] = {}
        carrito_sesion = session['carrito']
        prod_id_str = str(producto_id)
        carrito_sesion[prod_id_str] = carrito_sesion.get(prod_id_str, 0) + 1
        session.modified = True
        exito = True
    
    if exito:
        flash("¡Producto agregado a tu carrito exitosamente!", "success")
    else:
        flash("Hubo un error al agregar el producto al carrito. Inténtalo de nuevo.", "danger")
        
    return redirect(request.referrer or url_for('main.index'))

@main.route('/carrito/eliminar/<int:producto_id>', methods=['POST', 'GET'])
def eliminar_del_carrito(producto_id):
    """
    Elimina un producto del carrito real (BD) o temporal (sesión).
    """
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        exito = carrito_repo.eliminar_producto(usuario_id, producto_id)
    else:
        # Eliminar del carrito temporal de sesión
        carrito_sesion = session.get('carrito', {})
        prod_id_str = str(producto_id)
        if prod_id_str in carrito_sesion:
            del carrito_sesion[prod_id_str]
            session.modified = True
            exito = True
        else:
            exito = False
    
    if exito:
        flash("Producto retirado del carrito exitosamente.", "success")
    else:
        flash("No se pudo retirar el producto. Inténtalo nuevamente.", "danger")
        
    return redirect(url_for('main.carrito'))

@main.route('/carrito/comprar', methods=['POST', 'GET'])
def checkout_carrito():
    """
    Simulación de compra real: Vacía el carrito del usuario (BD) o de la sesión.
    """
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        exito = carrito_repo.vaciar_carrito(usuario_id)
    else:
        # Vaciar carrito temporal de sesión
        if 'carrito' in session:
            del session['carrito']
            session.modified = True
        exito = True
    
    if exito:
        flash("¡Tu compra ha sido procesada con éxito! Gracias por preferir TiendaPOO.", "success")
    else:
        flash("Hubo un problema al procesar tu pedido. Inténtalo de nuevo.", "danger")
        
    return redirect(url_for('main.index'))

@main.route('/ropa')
def seccion_ropa():
    """
    Ruta para la sección exclusiva de Ropa.
    """
    todos = producto_repo.obtener_todos_activos()
    # Filtramos por clase Ropa y que no sea calzado (talla no es un número de zapato)
    productos = [p for p in todos if p.__class__.__name__.lower() == 'ropa' and not p.talla.isdigit()]
    return render_template(
        'index.html', 
        productos=productos, 
        titulo_seccion="Moda y Ropa Exclusiva",
        descripcion_seccion="Prendas de vestir exclusivas, abrigos, chaquetas y camisetas diseñadas con materiales premium.",
        categoria_activa="ropa"
    )

@main.route('/calzado')
def seccion_calzado():
    """
    Ruta para la sección exclusiva de Calzado.
    """
    todos = producto_repo.obtener_todos_activos()
    # Filtramos por calzado (talla es un número de zapato)
    productos = [p for p in todos if p.__class__.__name__.lower() == 'ropa' and p.talla.isdigit()]
    return render_template(
        'index.html', 
        productos=productos, 
        titulo_seccion="Calzado y Zapatos Premium",
        descripcion_seccion="Nuestra colección exclusiva de tenis deportivos, botas todoterreno y zapatos de cuero artesanal.",
        categoria_activa="calzado"
    )

@main.route('/accesorios')
def seccion_accesorios():
    """
    Ruta para la sección exclusiva de Accesorios.
    """
    todos = producto_repo.obtener_todos_activos()
    # Filtramos por clase Electronico (relojes, auriculares)
    productos = [p for p in todos if p.__class__.__name__.lower() == 'electronico']
    return render_template(
        'index.html', 
        productos=productos, 
        titulo_seccion="Accesorios y Gadgets Exclusivos",
        descripcion_seccion="Relojes inteligentes, auriculares con cancelación de ruido y los mejores complementos para tu estilo.",
        categoria_activa="accesorios"
    )

@main.route('/ofertas')
def seccion_ofertas():
    """
    Ruta para ver los productos con descuentos y promociones especiales.
    """
    todos = producto_repo.obtener_todos_activos()
    # Filtramos productos que tienen oferta (en este caso, productos con ID par)
    productos = [p for p in todos if p.id % 2 == 0]
    return render_template(
        'index.html', 
        productos=productos, 
        titulo_seccion="Promociones y Ofertas Especiales",
        descripcion_seccion="Aprovecha nuestros descuentos de hasta el 20% en prendas y artículos seleccionados por tiempo limitado.",
        categoria_activa="ofertas"
    )

@main.route('/favoritos')
def favoritos():
    """
    Ruta de Lista de Deseos (Favoritos). Carga los productos guardados en la sesión.
    """
    favoritos_ids = session.get('favoritos', [])
    productos = []
    for prod_id in favoritos_ids:
        producto = producto_repo.obtener_por_id(int(prod_id))
        if producto:
            productos.append(producto)
            
    return render_template('favoritos.html', productos=productos)

@main.route('/favoritos/agregar/<int:producto_id>', methods=['POST', 'GET'])
def agregar_a_favoritos(producto_id):
    """
    Añade un producto a la lista de favoritos en la sesión del navegador.
    """
    if 'favoritos' not in session:
        session['favoritos'] = []
    
    favoritos_ids = session['favoritos']
    if producto_id not in favoritos_ids:
        favoritos_ids.append(producto_id)
        session.modified = True
        flash("¡Producto añadido a tus favoritos!", "success")
    else:
        flash("El producto ya se encuentra en tus favoritos.", "info")
        
    return redirect(request.referrer or url_for('main.index'))

@main.route('/favoritos/eliminar/<int:producto_id>', methods=['POST', 'GET'])
def eliminar_de_favoritos(producto_id):
    """
    Remueve un producto de la lista de favoritos de la sesión.
    """
    favoritos_ids = session.get('favoritos', [])
    if producto_id in favoritos_ids:
        favoritos_ids.remove(producto_id)
        session.modified = True
        flash("Producto removido de tus favoritos.", "success")
        
    return redirect(request.referrer or url_for('main.favoritos'))

