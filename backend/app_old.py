"""
Flask Application Entry Point
"""
import os
from dotenv import load_dotenv

# Load environment variables BEFORE importing config
load_dotenv()

from flask import Flask
from flask_cors import CORS
from config import get_config
from models import db
from controllers import project_bp, page_bp, template_bp, export_bp, file_bp


def create_app(config_class=None):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    # Ensure instance folder exists and set absolute database path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    instance_path = os.path.join(backend_dir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Override database URI with absolute path
    if not os.getenv('DATABASE_URL'):
        db_file = os.path.join(instance_path, 'database.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(project_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(template_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(file_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'Banana Slides API is running'}
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'name': 'Banana Slides API',
            'version': '1.0.0',
            'description': 'AI-powered PPT generation service',
            'endpoints': {
                'health': '/health',
                'api_docs': '/api',
                'projects': '/api/projects'
            }
        }
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    # Run development server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"""
    ╔══════════════════════════════════════╗
    ║   🍌 Banana Slides API Server 🍌   ║
    ╚══════════════════════════════════════╝
    
    Server starting on: http://localhost:{port}
    Environment: {os.getenv('FLASK_ENV', 'development')}
    Debug mode: {debug}
    
    API Base URL: http://localhost:{port}/api
    """)
    
    # Disable reloader to avoid database path issues in WSL
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)

