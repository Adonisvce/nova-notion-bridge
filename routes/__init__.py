# Route blueprint registrations
from .dynamic import dynamic_bp
from .logic_sync import logic_sync_bp
from .validate_plugins import validate_bp
from .command_center import command_center_bp
endpoint_router_bp = None
def register_all_routes(app):
    app.register_blueprint(dynamic_bp)
    app.register_blueprint(logic_sync_bp)
    app.register_blueprint(validate_bp)
    app.register_blueprint(command_center_bp)
