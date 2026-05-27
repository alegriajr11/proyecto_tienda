from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.producto import DescuentoPorcentaje, SinDescuento, Accesorio, Ropa, Zapato
from models.producto_repository import ProductoRepository
from models.usuario_repository import UsuarioRepository
from models.carrito_repository import CarritoRepository
from models.slide_repository import SlideRepository
from models.exceptions import TiendaError, AuthenticationError, EntityNotFoundError

def login_required(f):
    """
    Decorador de seguridad para proteger rutas que requieren autenticación.
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

# Instanciamos los repositorios (Singleton en Database asegura eficiencia)
producto_repo = ProductoRepository()
usuario_repo = UsuarioRepository()
carrito_repo = CarritoRepository()
slide_repo = SlideRepository()

@main.context_processor
def inject_cart_count():
    cantidad_total = 0
    try:
        if 'usuario_id' in session:
            cantidad_total = carrito_repo.obtener_cantidad_total(session['usuario_id'])
        else:
            carrito_sesion = session.get('carrito', {})
            cantidad_total = sum(int(cant) for cant in carrito_sesion.values())
    except TiendaError:
        cantidad_total = 0
    return dict(cart_count=cantidad_total)

@main.route('/')
def index():
    """
    Ruta principal (Catálogo). Filtra dinámicamente los productos por categoría.
    Aplica el patrón Strategy para las ofertas.
    """
    try:
        categoria_filtro = request.args.get('categoria')
        todos = producto_repo.obtener_todos_activos()
        
        titulo_seccion = None
        descripcion_seccion = None
        
        if categoria_filtro:
            filtro = categoria_filtro.lower().strip()
            productos = []
            for p in todos:
                clase = p.__class__.__name__.lower()
                if filtro == 'ropa' and clase == 'ropa':
                    productos.append(p)
                elif filtro == 'accesorios' and clase == 'accesorio':
                    productos.append(p)
                elif filtro == 'calzado' and clase == 'zapato':
                    productos.append(p)
                elif filtro == 'ofertas':
                    p.establecer_descuento(DescuentoPorcentaje(20))
                    productos.append(p)
            
            if filtro == 'ropa':
                titulo_seccion = "Moda y Ropa Exclusiva"
                descripcion_seccion = "Prendas de vestir exclusivas, abrigos, chaquetas y camisetas diseñadas con materiales premium."
            elif filtro == 'calzado':
                titulo_seccion = "Calzado y Zapatos Premium"
                descripcion_seccion = "Nuestra colección exclusiva de tenis deportivos, botas todoterreno y zapatos de cuero artesanal."
            elif filtro == 'accesorios':
                titulo_seccion = "Accesorios Exclusivos"
                descripcion_seccion = "Relojes inteligentes, auriculares con cancelación de ruido y los mejores complementos para tu estilo."
            elif filtro == 'ofertas':
                titulo_seccion = "Promociones y Ofertas Especiales"
                descripcion_seccion = "Aprovecha nuestros descuentos del 20% en artículos seleccionados por tiempo limitado."
            
            if not productos:
                productos = todos
                categoria_filtro = None
        else:
            productos = todos
        
        slides = slide_repo.obtener_activos() if not categoria_filtro else []
        
        return render_template(
            'index.html', 
            productos=productos, 
            categoria_activa=categoria_filtro,
            titulo_seccion=titulo_seccion,
            descripcion_seccion=descripcion_seccion,
            slides=slides
        )
    except TiendaError as e:
        flash(f"Error al cargar el catálogo: {e.mensaje}", "danger")
        return render_template('index.html', productos=[], slides=[])

@main.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    try:
        producto = producto_repo.obtener_por_id(producto_id)
        todos = producto_repo.obtener_todos_activos()
        relacionados = [p for p in todos if isinstance(p, producto.__class__) and p.id != producto.id][:4]
        
        return render_template(
            'producto_detalle.html',
            producto=producto,
            relacionados=relacionados
        )
    except EntityNotFoundError as e:
        flash(e.mensaje, "warning")
        return redirect(url_for('main.index'))
    except TiendaError as e:
        flash(f"Error al cargar el producto: {e.mensaje}", "danger")
        return redirect(url_for('main.index'))

@main.route('/contactos', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        flash(f"¡Gracias por tu mensaje, {nombre}! Nos pondremos en contacto pronto.", "success")
        return redirect(url_for('main.contacto'))
    return render_template('contact.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        if session.get('usuario_rol') == 'administrador':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        try:
            correo = request.form.get('correo')
            contrasena = request.form.get('contrasena')
            usuario = usuario_repo.verificar_contrasena(correo, contrasena)
            
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            session['usuario_rol'] = usuario.rol
            
            carrito_sesion = session.get('carrito', {})
            if carrito_sesion:
                for prod_id_str, cant in carrito_sesion.items():
                    carrito_repo.agregar_producto(usuario.id, int(prod_id_str), cantidad=cant)
                session.pop('carrito', None)
                session.modified = True
            
            flash(f"¡Bienvenido, {usuario.nombre}!", "success")
            if usuario.rol == 'administrador':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))
        except AuthenticationError as e:
            flash(e.mensaje, "danger")
        except TiendaError as e:
            flash(f"Error de sistema: {e.mensaje}", "danger")
            
    return render_template('login.html')

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'usuario_id' in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            correo = request.form.get('correo')
            contrasena = request.form.get('contrasena')
            confirmar = request.form.get('confirmar')
            
            if contrasena != confirmar:
                flash("Las contraseñas no coinciden.", "danger")
                return render_template('register.html')
                
            if usuario_repo.buscar_por_correo(correo):
                flash("El correo ya está registrado.", "danger")
                return render_template('register.html')
                
            if usuario_repo.crear_usuario(nombre, '', correo, '', contrasena):
                flash("Cuenta creada exitosamente.", "success")
                return redirect(url_for('main.login'))
            else:
                flash("Error al crear la cuenta.", "danger")
        except TiendaError as e:
            flash(f"Error al registrarse: {e.mensaje}", "danger")
            
    return render_template('register.html')

@main.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for('main.index'))

@main.route('/carrito')
def carrito():
    try:
        if 'usuario_id' in session:
            items = carrito_repo.obtener_carrito(session['usuario_id'])
        else:
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
        
        subtotal = sum(float(item['precio_venta']) * int(item['cantidad']) for item in items)
        gastos_envio = 15.00 if subtotal < 500.00 and subtotal > 0 else 0.00
        total = subtotal + gastos_envio
        
        return render_template('cart.html', items=items, subtotal=subtotal, gastos_envio=gastos_envio, total=total)
    except TiendaError as e:
        flash(f"Error al cargar el carrito: {e.mensaje}", "danger")
        return redirect(url_for('main.index'))

@main.route('/carrito/agregar/<int:producto_id>', methods=['POST', 'GET'])
def agregar_al_carrito(producto_id):
    try:
        if 'usuario_id' in session:
            exito = carrito_repo.agregar_producto(session['usuario_id'], producto_id, cantidad=1)
        else:
            if 'carrito' not in session:
                session['carrito'] = {}
            carrito_sesion = session['carrito']
            prod_id_str = str(producto_id)
            carrito_sesion[prod_id_str] = carrito_sesion.get(prod_id_str, 0) + 1
            session.modified = True
            exito = True
        
        if exito:
            flash("Producto agregado al carrito.", "success")
    except TiendaError as e:
        flash(f"Error al agregar al carrito: {e.mensaje}", "danger")
    return redirect(request.referrer or url_for('main.index'))

@main.route('/carrito/eliminar/<int:producto_id>', methods=['POST', 'GET'])
def eliminar_del_carrito(producto_id):
    try:
        if 'usuario_id' in session:
            exito = carrito_repo.eliminar_producto(session['usuario_id'], producto_id)
        else:
            carrito_sesion = session.get('carrito', {})
            prod_id_str = str(producto_id)
            if prod_id_str in carrito_sesion:
                del carrito_sesion[prod_id_str]
                session.modified = True
                exito = True
            else:
                exito = False
        
        if exito:
            flash("Producto eliminado del carrito.", "success")
    except TiendaError as e:
        flash(f"Error al eliminar del carrito: {e.mensaje}", "danger")
    return redirect(url_for('main.carrito'))

@main.route('/carrito/comprar', methods=['POST', 'GET'])
def checkout_carrito():
    try:
        if 'usuario_id' in session:
            exito = carrito_repo.vaciar_carrito(session['usuario_id'])
        else:
            session.pop('carrito', None)
            exito = True
        
        if exito:
            flash("¡Compra procesada con éxito!", "success")
    except TiendaError as e:
        flash(f"Error al procesar la compra: {e.mensaje}", "danger")
    return redirect(url_for('main.index'))

@main.route('/ropa')
def seccion_ropa():
    try:
        todos = producto_repo.obtener_todos_activos()
        productos = [p for p in todos if type(p) is Ropa]
        return render_template('index.html', productos=productos, titulo_seccion="Moda y Ropa Exclusiva", categoria_activa="ropa")
    except TiendaError as e:
        flash(f"Error: {e.mensaje}", "danger")
        return redirect(url_for('main.index'))

@main.route('/calzado')
def seccion_calzado():
    try:
        todos = producto_repo.obtener_todos_activos()
        productos = [p for p in todos if isinstance(p, Zapato)]
        return render_template('index.html', productos=productos, titulo_seccion="Calzado y Zapatos Premium", categoria_activa="calzado")
    except TiendaError as e:
        flash(f"Error: {e.mensaje}", "danger")
        return redirect(url_for('main.index'))

@main.route('/accesorios')
def seccion_accesorios():
    try:
        todos = producto_repo.obtener_todos_activos()
        productos = [p for p in todos if isinstance(p, Accesorio)]
        return render_template('index.html', productos=productos, titulo_seccion="Accesorios Exclusivos", categoria_activa="accesorios")
    except TiendaError as e:
        flash(f"Error: {e.mensaje}", "danger")
        return redirect(url_for('main.index'))

@main.route('/ofertas')
def seccion_ofertas():
    try:
        todos = producto_repo.obtener_todos_activos()
        estrategia = DescuentoPorcentaje(20)
        for p in todos:
            p.establecer_descuento(estrategia)
        return render_template('index.html', productos=todos, titulo_seccion="Promociones y Ofertas Especiales", categoria_activa="ofertas")
    except TiendaError as e:
        flash(f"Error: {e.mensaje}", "danger")
        return redirect(url_for('main.index'))

@main.route('/favoritos')
def favoritos():
    try:
        favoritos_ids = session.get('favoritos', [])
        productos = []
        for pid in favoritos_ids:
            try:
                p = producto_repo.obtener_por_id(int(pid))
                if p: productos.append(p)
            except EntityNotFoundError:
                continue
        return render_template('favoritos.html', productos=productos)
    except TiendaError as e:
        flash(f"Error: {e.mensaje}", "danger")
        return redirect(url_for('main.index'))

@main.route('/favoritos/agregar/<int:producto_id>', methods=['POST', 'GET'])
def agregar_a_favoritos(producto_id):
    if 'favoritos' not in session:
        session['favoritos'] = []
    if producto_id not in session['favoritos']:
        session['favoritos'].append(producto_id)
        session.modified = True
        flash("Añadido a favoritos.", "success")
    return redirect(request.referrer or url_for('main.index'))

@main.route('/favoritos/eliminar/<int:producto_id>', methods=['POST', 'GET'])
def eliminar_de_favoritos(producto_id):
    if 'favoritos' in session and producto_id in session['favoritos']:
        session['favoritos'].remove(producto_id)
        session.modified = True
        flash("Eliminado de favoritos.", "success")
    return redirect(request.referrer or url_for('main.favoritos'))
