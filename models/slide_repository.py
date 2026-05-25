# Repositorio de Slides (slide_repository.py)
#
# Principios SOLID:
# 1. SRP: Se encarga exclusivamente de la persistencia de los slides del banner.
# 2. DIP: Los controladores dependen de este repositorio, no de consultas SQL directas.

from models.database import Database


class SlideRepository:
    """
    Repositorio para gestionar los slides del banner promocional.
    """
    def __init__(self):
        self.db = Database()

    def obtener_activos(self):
        """Obtiene todos los slides activos ordenados por su posición."""
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
                print(f"[SlideRepository Error] Error al obtener slides activos: {e}")
            finally:
                conn.close()
        
        return slides

    def obtener_todos(self):
        """Obtiene todos los slides (activos e inactivos) para el admin."""
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
                print(f"[SlideRepository Error] Error al obtener todos los slides: {e}")
            finally:
                conn.close()
        
        return slides

    def obtener_por_id(self, slide_id):
        """Obtiene un slide por su ID."""
        conn = self.db.connect()
        slide = None
        
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM slides WHERE id = %s", (slide_id,))
                slide = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print(f"[SlideRepository Error] Error al obtener slide {slide_id}: {e}")
            finally:
                conn.close()
        
        return slide

    def crear(self, datos, usuario_id=None):
        """Crea un nuevo slide."""
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
                print(f"[SlideRepository Error] Error al crear slide: {e}")
                return False
            finally:
                conn.close()
        
        return False

    def actualizar(self, slide_id, datos):
        """Actualiza un slide existente."""
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
                print(f"[SlideRepository Error] Error al actualizar slide {slide_id}: {e}")
                return False
            finally:
                conn.close()
        
        return False

    def eliminar(self, slide_id):
        """Elimina un slide permanentemente."""
        conn = self.db.connect()
        
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM slides WHERE id = %s", (slide_id,))
                conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"[SlideRepository Error] Error al eliminar slide {slide_id}: {e}")
                return False
            finally:
                conn.close()
        
        return False
