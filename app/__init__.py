"""Team Manager server application"""

from flask import Flask

from app import extensions, views
from app.config import DefaultConfig


def create_app():
    """Create application"""
    app = Flask('Team manager')

    app.config.from_object(DefaultConfig)
    # Override config with optional settings file
    app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)

    api = extensions.create_api(app)
    views.register_blueprints(api)

    return app
