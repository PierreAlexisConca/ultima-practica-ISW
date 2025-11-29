"""
Rutas y controladores de la aplicación
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.database import (
    insert_lead, get_all_leads, get_lead_by_id, 
    update_lead, delete_lead, close_db_connection
)

bp = Blueprint('main', __name__)

# Cerrar conexión DB al final de cada request
@bp.teardown_app_request
def teardown_db(exception=None):
    close_db_connection(exception)

@bp.route('/')
def index():
    """Página principal con formulario de registro"""
    return render_template('index.html')

@bp.route('/leads')
def leads_list():
    """Página que muestra todos los leads registrados"""
    leads = get_all_leads()
    return render_template('leads.html', leads=leads)

@bp.route('/api/leads', methods=['POST'])
def create_lead():
    """
    API endpoint para crear un nuevo lead
    Espera JSON con: nombre_completo, correo_electronico, telefono, interes
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['nombre_completo', 'correo_electronico', 'telefono', 'interes']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'El campo {field} es requerido'
                }), 400
        
        # Validar formato de correo básico
        if '@' not in data['correo_electronico']:
            return jsonify({
                'success': False,
                'message': 'Correo electrónico inválido'
            }), 400
        
        # Insertar lead
        success, message, lead_id = insert_lead(
            data['nombre_completo'],
            data['correo_electronico'],
            data['telefono'],
            data['interes']
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'lead_id': lead_id
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }), 500

@bp.route('/api/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Obtiene información de un lead específico"""
    lead = get_lead_by_id(lead_id)
    
    if lead:
        return jsonify({
            'success': True,
            'lead': dict(lead)
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Lead no encontrado'
        }), 404

@bp.route('/api/leads/<int:lead_id>', methods=['PUT'])
def update_lead_route(lead_id):
    """Actualiza un lead existente"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['nombre_completo', 'correo_electronico', 'telefono', 'interes']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'El campo {field} es requerido'
                }), 400
        
        success, message = update_lead(
            lead_id,
            data['nombre_completo'],
            data['correo_electronico'],
            data['telefono'],
            data['interes']
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }), 500

@bp.route('/api/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead_route(lead_id):
    """Elimina un lead"""
    try:
        success, message = delete_lead(lead_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }), 500

@bp.route('/api/leads', methods=['GET'])
def get_all_leads_api():
    """Obtiene todos los leads en formato JSON"""
    leads = get_all_leads()
    return jsonify({
        'success': True,
        'leads': [dict(lead) for lead in leads]
    })
