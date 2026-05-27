from models.database import Database
from models.interfaces import ISlideRepository
from models.exceptions import RepositoryError

class SlideRepository(ISlideRepository):
    """
    Repositorio para gestionar los slides del banner promocional.
    Implementa ISlideRepository para seguir DIP.
    """
    def __init__(self):
        self.db = Database()

    def obtener_activos(self):
        try:
            conn = self.db.connect()
            slides = []
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT s.*, u.nombre AS autor_nombre
                        FROM slides s
                        LEFT JOIN usuarios u ON s.creado_por = u.id
                        WHERE s.activo = TRUE
                        ORDER BY s.orden ASC
                    """)
                    slides = cursor.fetchall()
                    cursor.close()
                except Exception as e:
                    raise RepositoryError(f"Error al obtener slides activos: {str(e)}")
                finally:
                    conn.close()
            return slides
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def obtener_todos(self):
        try:
            conn = self.db.connect()
            slides = []
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT s.*, u.nombre AS autor_nombre
                        FROM slides s
                        LEFT JOIN usuarios u ON s.creado_por = u.id
                        ORDER BY s.orden ASC
                    """)
                    slides = cursor.fetchall()
                    cursor.close()
                except Exception as e:
                    raise RepositoryError(f"Error al obtener todos los slides: {str(e)}")
                finally:
                    conn.close()
            return slides
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def obtener_por_id(self, slide_id):
        try:
            conn = self.db.connect()
            slide = None
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT * FROM slides WHERE id = %s", (slide_id,))
                    slide = cursor.fetchone()
                    cursor.close()
                except Exception as e:
                    raise RepositoryError(f"Error al obtener slide {slide_id}: {str(e)}")
                finally:
                    conn.close()
            return slide
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def crear(self, datos, usuario_id=None):
        try:
            conn = self.db.connect()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO slides (titulo, subtitulo, imagen_url, texto_boton, enlace_boton, posicion_texto, orden, activo, creado_por)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        datos.get('titulo'),
                        datos.get('subtitulo'),
                        datos.get('imagen_url'),
                        datos.get('texto_boton', 'Ver Catálogo'),
                        datos.get('enlace_boton', '/'),
                        datos.get('posicion_texto', 'izquierda'),
                        datos.get('orden', 0),
                        datos.get('activo', True),
                        usuario_id
                    ))
                    conn.commit()
                    cursor.close()
                    return True
                except Exception as e:
                    raise RepositoryError(f"Error al crear slide: {str(e)}")
                finally:
                    conn.close()
            return False
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def actualizar(self, slide_id, datos):
        try:
            conn = self.db.connect()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE slides SET titulo=%s, subtitulo=%s, imagen_url=%s, texto_boton=%s,
                        enlace_boton=%s, posicion_texto=%s, orden=%s, activo=%s
                        WHERE id=%s
                    """, (
                        datos.get('titulo'),
                        datos.get('subtitulo'),
                        datos.get('imagen_url'),
                        datos.get('texto_boton', 'Ver Catálogo'),
                        datos.get('enlace_boton', '/'),
                        datos.get('posicion_texto', 'izquierda'),
                        datos.get('orden', 0),
                        datos.get('activo', True),
                        slide_id
                    ))
                    conn.commit()
                    cursor.close()
                    return True
                except Exception as e:
                    raise RepositoryError(f"Error al actualizar slide {slide_id}: {str(e)}")
                finally:
                    conn.close()
            return False
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")

    def eliminar(self, slide_id):
        try:
            conn = self.db.connect()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM slides WHERE id = %s", (slide_id,))
                    conn.commit()
                    cursor.close()
                    return True
                except Exception as e:
                    raise RepositoryError(f"Error al eliminar slide {slide_id}: {str(e)}")
                finally:
                    conn.close()
            return False
        except Exception as e:
            raise RepositoryError(f"Error de base de datos: {str(e)}")
