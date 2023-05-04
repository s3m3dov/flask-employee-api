"""Modules initialization"""

from . import members
from . import teams

MODULES = (
    teams,
    members
)


def register_blueprints(api):
    """Initialize application with all modules"""
    for module in MODULES:
        api.register_blueprint(module.blp)
