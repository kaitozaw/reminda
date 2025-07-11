from flask import Blueprint
import importlib
import pkgutil

def register_routes(app):
    from app import routes
    for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
        module = importlib.import_module(f"app.routes.{module_name}")

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Blueprint):
                app.register_blueprint(attr)