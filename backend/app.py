import os
from flask import Flask
from flask_cors import CORS
from api.routes import api_blueprint
from api.error_handlers import register_error_handlers
import config


def create_app():
    app = Flask(__name__)

    env_name = os.getenv('FLASK_ENV', 'development').lower()
    app_config = config.config_by_name.get(env_name, config.config_by_name['default'])
    app.config.from_object(app_config)

    cors_origins = app.config['CORS_ORIGINS']

    CORS(
        app,
        resources={r"/*": {"origins": cors_origins}},
        supports_credentials=False,
        methods=['GET', 'POST', 'OPTIONS'],
        allow_headers=['Content-Type'],
    )

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix=app.config['API_BASE_PATH'])

    # Register error handlers
    register_error_handlers(app)

    # Health check endpoint
    @app.route('/health')
    def health():
        return {
            'status': 'healthy',
            'service': 'speedread-backend',
            'version': '1.0.0',
            'environment': app.config['ENV'],
        }, 200

    @app.route('/')
    def index():
        return {
            'service': 'SpeedRead Backend API',
            'version': '1.0.0',
            'environment': app.config['ENV'],
            'endpoints': {
                'health': '/health',
                'process_text': '/api/process-text',
                'calculate_orp': '/api/calculate-orp',
            },
            'documentation': 'See README.md for full API documentation',
        }, 200

    return app


if __name__ == '__main__':
    app = create_app()

    # Get port from environment (Render assigns this)
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print('=' * 60)
    print('SpeedRead Backend API')
    print('=' * 60)
    print(f"Server running on: http://0.0.0.0:{port}")
    print(f"Debug mode: {debug}")
    print('=' * 60)

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
    )
