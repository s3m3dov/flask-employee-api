from . import employees

MODULES = (
    employees,
)


def register_blueprints(app):
    """Initialize application with all modules"""
    for module in MODULES:
        app.register_blueprint(module.blp)
