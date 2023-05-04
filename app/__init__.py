"""Team Manager server application"""
from typing import Optional, Dict, Any

from flask import Flask

from app import extensions, views
from app.config import ProductionConfig, DebugConfig


def create_app(test_config: Optional[Dict[str, Any]] = None):
    """Create application"""
    app = Flask("Team manager")

    # Loading config...
    # Load defaults
    _config = app.config
    flask_debug: bool = _config.get("DEBUG", False)
    if flask_debug:
        _config.from_object(DebugConfig)
    elif test_config is None:
        # only load production defaults if no special test config is given
        _config.from_object(ProductionConfig)
    # Override config with optional settings file
    app.config.from_envvar("FLASK_SETTINGS_FILE", silent=True)

    api = extensions.create_api(app)
    views.register_blueprints(api)

    return app
