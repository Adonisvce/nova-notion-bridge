from flask import Flask

# Import route blueprints
from .command_center import command_center_bp
from .endpoint_router import endpoint_router_bp
from .dynamic import dynamic_bp
from .validate_plugins import validate_bp
from .logic_sync import logic_sync_bp

def register_all_routes(app: Flask):
    app.register_blueprint(command_center_bp)
    app.register_blueprint(endpoint_router_bp)
    app.register_blueprint(dynamic_bp)
    app.register_blueprint(validate_bp)
    app.register_blueprint(logic_sync_bp)

