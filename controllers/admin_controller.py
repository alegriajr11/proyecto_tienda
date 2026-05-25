# Controlador de Administración (admin_controller.py)
#
# Principios SOLID aplicados:
# 1. SRP: Este controlador se encarga exclusivamente de las rutas del panel de administración.
#    Está completamente separado del controlador de la tienda cliente.
# 2. DIP: Consume los repositorios existentes para interactuar con la base de datos.
# 3. OCP: Nuevas secciones del admin se pueden agregar sin modificar las existentes.

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.producto_repository import ProductoRepository
from models.usuario_repository import UsuarioRepository
from models.slide_repository import SlideRepository
from models.database import Database

# Blueprint separado con prefijo /admin
admin = Blueprint('admin', __name__, url_prefix='/admin')

# Repositorios
producto_repo = ProductoRepository()
usuario_repo = UsuarioRepository()
slide_repo = SlideRepository()
db = Database()


def admin_required(f):
    """
    Decorador de seguridad para proteger rutas del panel de administración.
    Verifica que el usuario tenga sesión activa y rol de administrador.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Debes iniciar sesión para acceder al panel de administración.", "warning")
            return redirect(url_for('main.login'))
        if session.get('usuario_rol') != 'administrador':
            flash("No tienes permisos para acceder al panel de administración.", "danger")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/')
@admin_required
def dashboard():
    """Panel principal del administrador con métricas generales."""
    conn = db.connect()
    stats = {
        'total_productos': 0,
        'productos_activos': 0,
        'productos_inactivos': 0,
        'bajo_stock': 0,
        'total_categorias': 0,
        'total_usuarios': 0,
    }
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT COUNT(*) as total FROM productos")
            stats['total_productos'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as total FROM productos WHERE estado = 'activo'")
            stats['productos_activos'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as total FROM productos WHERE estado = 'inactivo'")
            stats['productos_inactivos'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as total FROM productos WHERE stock_actual <= stock_minimo AND estado = 'activo'")
            stats['bajo_stock'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as total FROM categorias")
            stats['total_categorias'] = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as total FROM usuarios")
            stats['total_usuarios'] = cursor.fetchone()['total']
            
            cursor.close()
        except Exception as e:
            print(f"[Admin Error] Error al obtener estadísticas: {e}")
        finally:
            conn.close()
    
    return render_template('admin/dashboard.html', stats=stats)


@admin.route('/productos')
@admin_required
def productos():
    """Lista todos los productos con opciones de gestión."""
    conn = db.connect()
    productos = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.*, c.nombre AS categoria_nombre 
                FROM productos p 
                LEFT JOIN categorias c ON p.categoria_id = c.id
                ORDER BY p.id DESC
            """
            cursor.execute(query)
            productos = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"[Admin Error] Error al obtener productos: {e}")
        finally:
            conn.close()
    
    return render_template('admin/productos.html', productos=productos)


@admin.route('/productos/crear', methods=['GET', 'POST'])
@admin_required
def crear_producto():
    """Formulario para crear un nuevo producto."""
    conn = db.connect()
    categorias = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categorias ORDER BY nombre")
            categorias = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"[Admin Error] Error al obtener categorías: {e}")
        finally:
            conn.close()
    
    if request.method == 'POST':
        conn = db.connect()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO productos (nombre, categoria_id, descripcion, precio_compra, precio_venta, 
                    imagen, stock_actual, stock_minimo, marca, modelo, color, talla, garantia_dias, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    request.form.get('nombre'),
                    request.form.get('categoria_id') or None,
                    request.form.get('descripcion'),
                    request.form.get('precio_compra') or 0,
                    request.form.get('precio_venta'),
                    request.form.get('imagen'),
                    request.form.get('stock_actual') or 0,
                    request.form.get('stock_minimo') or 0,
                    request.form.get('marca') or None,
                    request.form.get('modelo') or None,
                    request.form.get('color') or None,
                    request.form.get('talla') or None,
                    request.form.get('garantia_dias') or None,
                    request.form.get('estado', 'activo')
                )
                cursor.execute(query, valores)
                conn.commit()
                cursor.close()
                flash("Producto creado exitosamente.", "success")
                return redirect(url_for('admin.productos'))
            except Exception as e:
                print(f"[Admin Error] Error al crear producto: {e}")
                flash(f"Error al crear el producto: {e}", "danger")
            finally:
                conn.close()
    
    return render_template('admin/producto_form.html', categorias=categorias, producto=None)


@admin.route('/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
@admin_required
def editar_producto(producto_id):
    """Formulario para editar un producto existente."""
    conn = db.connect()
    producto = None
    categorias = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
            producto = cursor.fetchone()
            cursor.execute("SELECT * FROM categorias ORDER BY nombre")
            categorias = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"[Admin Error] Error al obtener producto: {e}")
        finally:
            conn.close()
    
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for('admin.productos'))
    
    if request.method == 'POST':
        conn = db.connect()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    UPDATE productos SET nombre=%s, categoria_id=%s, descripcion=%s, precio_compra=%s,
                    precio_venta=%s, imagen=%s, stock_actual=%s, stock_minimo=%s, marca=%s, modelo=%s,
                    color=%s, talla=%s, garantia_dias=%s, estado=%s
                    WHERE id=%s
                """
                valores = (
                    request.form.get('nombre'),
                    request.form.get('categoria_id') or None,
                    request.form.get('descripcion'),
                    request.form.get('precio_compra') or 0,
                    request.form.get('precio_venta'),
                    request.form.get('imagen'),
                    request.form.get('stock_actual') or 0,
                    request.form.get('stock_minimo') or 0,
                    request.form.get('marca') or None,
                    request.form.get('modelo') or None,
                    request.form.get('color') or None,
                    request.form.get('talla') or None,
                    request.form.get('garantia_dias') or None,
                    request.form.get('estado', 'activo'),
                    producto_id
                )
                cursor.execute(query, valores)
                conn.commit()
                cursor.close()
                flash("Producto actualizado exitosamente.", "success")
                return redirect(url_for('admin.productos'))
            except Exception as e:
                print(f"[Admin Error] Error al actualizar producto: {e}")
                flash(f"Error al actualizar el producto: {e}", "danger")
            finally:
                conn.close()
    
    return render_template('admin/producto_form.html', categorias=categorias, producto=producto)


@admin.route('/productos/eliminar/<int:producto_id>', methods=['POST'])
@admin_required
def eliminar_producto(producto_id):
    """Elimina (desactiva) un producto."""
    conn = db.connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET estado = 'inactivo' WHERE id = %s", (producto_id,))
            conn.commit()
            cursor.close()
            flash("Producto desactivado exitosamente.", "success")
        except Exception as e:
            print(f"[Admin Error] Error al eliminar producto: {e}")
            flash("Error al desactivar el producto.", "danger")
        finally:
            conn.close()
    
    return redirect(url_for('admin.productos'))


@admin.route('/categorias')
@admin_required
def categorias():
    """Lista todas las categorías."""
    conn = db.connect()
    categorias = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT c.*, COUNT(p.id) as total_productos 
                FROM categorias c 
                LEFT JOIN productos p ON c.id = p.categoria_id
                GROUP BY c.id
                ORDER BY c.nombre
            """
            cursor.execute(query)
            categorias = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"[Admin Error] Error al obtener categorías: {e}")
        finally:
            conn.close()
    
    return render_template('admin/categorias.html', categorias=categorias)


@admin.route('/categorias/crear', methods=['POST'])
@admin_required
def crear_categoria():
    """Crea una nueva categoría."""
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    
    if not nombre:
        flash("El nombre de la categoría es obligatorio.", "danger")
        return redirect(url_for('admin.categorias'))
    
    conn = db.connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
            conn.commit()
            cursor.close()
            flash("Categoría creada exitosamente.", "success")
        except Exception as e:
            print(f"[Admin Error] Error al crear categoría: {e}")
            flash("Error al crear la categoría.", "danger")
        finally:
            conn.close()
    
    return redirect(url_for('admin.categorias'))


@admin.route('/categorias/eliminar/<int:categoria_id>', methods=['POST'])
@admin_required
def eliminar_categoria(categoria_id):
    """Elimina una categoría si no tiene productos asociados."""
    conn = db.connect()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM productos WHERE categoria_id = %s", (categoria_id,))
            resultado = cursor.fetchone()
            
            if resultado['total'] > 0:
                flash("No se puede eliminar una categoría con productos asociados.", "danger")
            else:
                cursor.execute("DELETE FROM categorias WHERE id = %s", (categoria_id,))
                conn.commit()
                flash("Categoría eliminada exitosamente.", "success")
            
            cursor.close()
        except Exception as e:
            print(f"[Admin Error] Error al eliminar categoría: {e}")
            flash("Error al eliminar la categoría.", "danger")
        finally:
            conn.close()
    
    return redirect(url_for('admin.categorias'))


@admin.route('/inventario')
@admin_required
def inventario():
    """Vista de gestión de inventario con alertas de stock."""
    conn = db.connect()
    productos = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.id, p.nombre, p.marca, p.stock_actual, p.stock_minimo, p.estado,
                       c.nombre AS categoria_nombre,
                       p.precio_compra, p.precio_venta
                FROM productos p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                WHERE p.estado = 'activo'
                ORDER BY (p.stock_actual <= p.stock_minimo) DESC, p.stock_actual ASC
            """
            cursor.execute(query)
            productos = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"[Admin Error] Error al obtener inventario: {e}")
        finally:
            conn.close()
    
    return render_template('admin/inventario.html', productos=productos)


@admin.route('/inventario/actualizar/<int:producto_id>', methods=['POST'])
@admin_required
def actualizar_stock(producto_id):
    """Actualiza el stock de un producto."""
    nuevo_stock = request.form.get('stock_actual')
    
    conn = db.connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET stock_actual = %s WHERE id = %s", (nuevo_stock, producto_id))
            conn.commit()
            cursor.close()
            flash("Stock actualizado exitosamente.", "success")
        except Exception as e:
            print(f"[Admin Error] Error al actualizar stock: {e}")
            flash("Error al actualizar el stock.", "danger")
        finally:
            conn.close()
    
    return redirect(url_for('admin.inventario'))


@admin.route('/usuarios')
@admin_required
def usuarios():
    """Lista todos los usuarios registrados."""
    conn = db.connect()
    usuarios = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre, apellido, correo, telefono, rol, fecha_registro FROM usuarios ORDER BY fecha_registro DESC")
            usuarios = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"[Admin Error] Error al obtener usuarios: {e}")
        finally:
            conn.close()
    
    return render_template('admin/usuarios.html', usuarios=usuarios)


# ═══════════════════════════════════════════════════════════════════
# GESTIÓN DE SLIDES DEL BANNER PROMOCIONAL
# ═══════════════════════════════════════════════════════════════════

@admin.route('/slides')
@admin_required
def slides():
    """Lista todos los slides del banner promocional."""
    todos_slides = slide_repo.obtener_todos()
    return render_template('admin/slides.html', slides=todos_slides)


@admin.route('/slides/crear', methods=['GET', 'POST'])
@admin_required
def crear_slide():
    """Formulario para crear un nuevo slide."""
    if request.method == 'POST':
        datos = {
            'titulo': request.form.get('titulo'),
            'subtitulo': request.form.get('subtitulo'),
            'imagen_url': request.form.get('imagen_url'),
            'texto_boton': request.form.get('texto_boton') or 'Ver Catálogo',
            'enlace_boton': request.form.get('enlace_boton') or '/',
            'posicion_texto': request.form.get('posicion_texto', 'izquierda'),
            'orden': request.form.get('orden') or 0,
            'activo': request.form.get('activo') == 'on'
        }
        
        exito = slide_repo.crear(datos, usuario_id=session.get('usuario_id'))
        if exito:
            flash("Slide creado exitosamente.", "success")
            return redirect(url_for('admin.slides'))
        else:
            flash("Error al crear el slide.", "danger")
    
    return render_template('admin/slide_form.html', slide=None)


@admin.route('/slides/editar/<int:slide_id>', methods=['GET', 'POST'])
@admin_required
def editar_slide(slide_id):
    """Formulario para editar un slide existente."""
    slide = slide_repo.obtener_por_id(slide_id)
    
    if not slide:
        flash("Slide no encontrado.", "danger")
        return redirect(url_for('admin.slides'))
    
    if request.method == 'POST':
        datos = {
            'titulo': request.form.get('titulo'),
            'subtitulo': request.form.get('subtitulo'),
            'imagen_url': request.form.get('imagen_url'),
            'texto_boton': request.form.get('texto_boton') or 'Ver Catálogo',
            'enlace_boton': request.form.get('enlace_boton') or '/',
            'posicion_texto': request.form.get('posicion_texto', 'izquierda'),
            'orden': request.form.get('orden') or 0,
            'activo': request.form.get('activo') == 'on'
        }
        
        exito = slide_repo.actualizar(slide_id, datos)
        if exito:
            flash("Slide actualizado exitosamente.", "success")
            return redirect(url_for('admin.slides'))
        else:
            flash("Error al actualizar el slide.", "danger")
    
    return render_template('admin/slide_form.html', slide=slide)


@admin.route('/slides/eliminar/<int:slide_id>', methods=['POST'])
@admin_required
def eliminar_slide(slide_id):
    """Elimina un slide permanentemente."""
    exito = slide_repo.eliminar(slide_id)
    if exito:
        flash("Slide eliminado exitosamente.", "success")
    else:
        flash("Error al eliminar el slide.", "danger")
    
    return redirect(url_for('admin.slides'))
