"""Modules initialization"""

from . import members
from . import teams
from . import employees

MODULES = (
    teams,
    members,
    employees,
)


def register_blueprints(api):
    """Initialize application with all modules"""
    for module in MODULES:
        api.register_blueprint(module.blp)
