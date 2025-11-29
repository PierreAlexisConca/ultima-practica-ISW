"""
Archivo principal para ejecutar la aplicación Flask
"""
from app import create_app
from app.database import init_db
import os

# Crear la aplicación
app = create_app()

# Inicializar la base de datos al arrancar
with app.app_context():
    try:
        init_db()
        print("✓ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"✗ Error al inicializar la base de datos: {e}")

if __name__ == '__main__':
    # Obtener el puerto del entorno o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    
    # Ejecutar la aplicación
    app.run(
        host='0.0.0.0',  # Permite conexiones desde cualquier IP
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )