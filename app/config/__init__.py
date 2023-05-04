"""Module containing default config values."""
import logging
from os import urandom

from .default import DefaultConfig, LogConfig
from .smorest_config import SmorestProductionConfig, SmorestDebugConfig
from .sqlalchemy_config import SQLAchemyProductionConfig, SQLAchemyDebugConfig


class MainConfig(DefaultConfig, LogConfig):
    API_TITLE = "Employees API"
    API_VERSION = 0.1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"


class ProductionConfig(MainConfig, SQLAchemyProductionConfig, SmorestProductionConfig):
    ENV = "production"
    SECRET_KEY = urandom(32)

    REVERSE_PROXY_COUNT = 0

    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.INFO

    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False


class DebugConfig(ProductionConfig, SQLAchemyDebugConfig, SmorestDebugConfig):
    ENV = "development"
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = (
        "debug_secret"  # FIXME make sure this NEVER! gets used in production!!!
    )
