import sqlalchemy as sa
from faker import Faker

from app.extensions.database import db


class Employee(db.Model):
    """Employee model class"""

    __tablename__ = "employees"
    __table_args__ = {"extend_existing": True}

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(length=50))
    department = sa.Column(sa.String(length=50))
    salary = sa.Column(sa.Float, nullable=False)
    hire_date = sa.Column(sa.DateTime, nullable=False)


def generate_employees(count: int = 50) -> None:
    faker = Faker()
    with db.session() as session:
        db.session.commit()
        for _ in range(count):
            employee = Employee()
            employee.name = faker.name()
            employee.department = faker.department()
            employee.salary = round(faker.uniform(30000, 1000000), 2)
            employee.hire_date = faker.date_time_between(
                start_date="-10y", end_date="now"
            )
            session.add(employee)
        session.commit()


if __name__ == "__main__":
    generate_employees()
