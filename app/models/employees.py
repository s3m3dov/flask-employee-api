import sqlalchemy as sa

from app.extensions.database import db


class Employee(db.Model):
    """Employee model class"""

    __tablename__ = "employees"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(length=50))
    department = sa.Column(sa.String(length=50))
    salary = sa.Column(sa.Float, nullable=False)
    hire_date = sa.Column(sa.DateTime, nullable=False)
