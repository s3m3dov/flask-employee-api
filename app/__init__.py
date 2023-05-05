"""Team Manager server application"""

from typing import Optional, Dict, Any

from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from http import HTTPStatus as status
from app import extensions, views, commands
from app import extensions, views, commands
from app.config import ProductionConfig, DebugConfig
from app.config import ProductionConfig, DebugConfig
from app.extensions.logger import LoggingConfig
from app.extensions.logger import LoggingConfig


def create_app(test_config: Optional[Dict[str, Any]] = None):
    """Create application"""
    app = Flask(__name__)

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

    # Configure logging
    logging_config = LoggingConfig(_config)
    logger = app.logger
    for _logger in (app.logger,):
        logging_config.configure(_logger)
        logger.setLevel(logging_config.LOG_LEVEL)

    logger.debug("Debug message")
    logger.info("Configuration loaded")

    # Register commands
    commands.register_blueprints(app)

    # Register extensions
    api = extensions.create_api(app)

    # Register views
    views.register_blueprints(api)

    # Exception handlers
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = jsonify(
            {
                "code": e.code,
                "status": e.name,
                "message": e.description,
            }
        )
        response.status_code = e.code
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        response = jsonify(
            {
                "code": status.BAD_REQUEST,
                "status": status.BAD_REQUEST.phrase,
                "message": e.messages,
            }
        )
        response.status_code = status.BAD_REQUEST
        return response

    return app
