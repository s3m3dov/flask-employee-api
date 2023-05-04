"""Relational database"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # pylint: disable=invalid-name


def init_app(app):
    """Initialize relational database extension"""
    db.init_app(app)
    # Create an application context
    with app.app_context():
        # Create all the tables in the database
        db.create_all()
