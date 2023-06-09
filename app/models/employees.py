import sqlalchemy as sa

from app.extensions.database import db


class Employee(db.Model):
    """Employee model class"""

    __tablename__ = "employees"
    __table_args__ = {"extend_existing": True}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(length=50), nullable=False)
    department = sa.Column(sa.String(length=50), nullable=False)
    salary = sa.Column(sa.Float, nullable=False, default=0.0)
    hire_date = sa.Column(sa.DateTime, nullable=False)
