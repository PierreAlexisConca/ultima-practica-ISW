"""
Inicialización de la aplicación Flask
Sistema de Gestión de Leads
"""
from flask import Flask
import os

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración de base de datos
    app.config['DB_HOST'] = os.environ.get('DB_HOST', 'leads-tracker-db.chrtzh6gakul.us-east-1.rds.amazonaws.com')
    app.config['DB_NAME'] = os.environ.get('DB_NAME', 'leadsdb')
    app.config['DB_USER'] = os.environ.get('DB_USER', 'postgres')
    app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD', 'ConcaFlores312007')
    app.config['DB_PORT'] = os.environ.get('DB_PORT', '5432')
    
    # Registrar rutas
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app
