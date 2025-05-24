from .dynamic import dynamic_bp
from .validate_plugins import validate_bp
from .logic_sync import logic_sync_bp

def register_all_routes(app):
    app.register_blueprint(dynamic_bp)
    app.register_blueprint(validate_bp)
    app.register_blueprint(logic_sync_bp)
