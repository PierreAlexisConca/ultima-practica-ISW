"""
Módulo de conexión y operaciones de base de datos
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app, g

def get_db_connection():
    """
    Obtiene una conexión a la base de datos PostgreSQL
    Utiliza el contexto 'g' de Flask para reutilizar la conexión
    """
    if 'db' not in g:
        try:
            g.db = psycopg2.connect(
                host=current_app.config['DB_HOST'],
                database=current_app.config['DB_NAME'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                port=current_app.config['DB_PORT']
            )
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise
    return g.db

def close_db_connection(e=None):
    """Cierra la conexión a la base de datos al final de la solicitud"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Inicializa la base de datos creando la tabla de leads si no existe
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Crear tabla de leads
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id SERIAL PRIMARY KEY,
            nombre_completo VARCHAR(255) NOT NULL,
            correo_electronico VARCHAR(255) UNIQUE NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            interes VARCHAR(255) NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    print("Base de datos inicializada correctamente")

def insert_lead(nombre, correo, telefono, interes):
    """
    Inserta un nuevo lead en la base de datos
    
    Args:
        nombre: Nombre completo del lead
        correo: Correo electrónico (debe ser único)
        telefono: Número de teléfono
        interes: Servicio o producto de interés
    
    Returns:
        tuple: (success: bool, message: str, lead_id: int or None)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO leads (nombre_completo, correo_electronico, telefono, interes)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        ''', (nombre, correo, telefono, interes))
        
        lead_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        
        return True, "Lead registrado exitosamente", lead_id
    
    except psycopg2.IntegrityError:
        conn.rollback()
        return False, "El correo electrónico ya está registrado", None
    except Exception as e:
        conn.rollback()
        return False, f"Error al registrar lead: {str(e)}", None

def get_all_leads():
    """
    Obtiene todos los leads de la base de datos
    
    Returns:
        list: Lista de diccionarios con información de leads
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('''
            SELECT id, nombre_completo, correo_electronico, telefono, 
                   interes, fecha_registro
            FROM leads
            ORDER BY fecha_registro DESC
        ''')
        
        leads = cursor.fetchall()
        cursor.close()
        
        return leads
    except Exception as e:
        print(f"Error al obtener leads: {e}")
        return []

def get_lead_by_id(lead_id):
    """
    Obtiene un lead específico por su ID
    
    Args:
        lead_id: ID del lead
    
    Returns:
        dict or None: Información del lead o None si no existe
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('''
            SELECT id, nombre_completo, correo_electronico, telefono, 
                   interes, fecha_registro
            FROM leads
            WHERE id = %s
        ''', (lead_id,))
        
        lead = cursor.fetchone()
        cursor.close()
        
        return lead
    except Exception as e:
        print(f"Error al obtener lead: {e}")
        return None

def update_lead(lead_id, nombre, correo, telefono, interes):
    """
    Actualiza un lead existente
    
    Args:
        lead_id: ID del lead a actualizar
        nombre: Nuevo nombre completo
        correo: Nuevo correo electrónico
        telefono: Nuevo teléfono
        interes: Nuevo interés
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE leads
            SET nombre_completo = %s, correo_electronico = %s, 
                telefono = %s, interes = %s
            WHERE id = %s
        ''', (nombre, correo, telefono, interes, lead_id))
        
        conn.commit()
        cursor.close()
        
        if cursor.rowcount > 0:
            return True, "Lead actualizado exitosamente"
        else:
            return False, "Lead no encontrado"
    
    except psycopg2.IntegrityError:
        conn.rollback()
        return False, "El correo electrónico ya está registrado"
    except Exception as e:
        conn.rollback()
        return False, f"Error al actualizar lead: {str(e)}"

def delete_lead(lead_id):
    """
    Elimina un lead de la base de datos
    
    Args:
        lead_id: ID del lead a eliminar
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM leads WHERE id = %s', (lead_id,))
        
        conn.commit()
        cursor.close()
        
        if cursor.rowcount > 0:
            return True, "Lead eliminado exitosamente"
        else:
            return False, "Lead no encontrado"
    
    except Exception as e:
        conn.rollback()
        return False, f"Error al eliminar lead: {str(e)}"
