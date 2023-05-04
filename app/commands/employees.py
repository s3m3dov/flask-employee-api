import random

import click
from faker import Faker
from flask import Blueprint

from app.constants import departments
from app.extensions.database import db
from app.models.employees import Employee

blp = Blueprint("employees", __name__, cli_group=None)


@blp.cli.command("generate-employees")
@click.option("--count", default=100, help="Number of employees to generate")
def generate_employees(count: int):
    """Generate random employees"""
    fake = Faker()

    with db.session() as session:
        for _ in range(count):
            employee = Employee()
            employee.name = fake.name()
            employee.department = random.choice(departments)
            employee.salary = fake.pyint(min_value=30000, max_value=1000000)
            employee.hire_date = fake.date_time_between(
                start_date="-10y", end_date="now"
            )
            session.add(employee)
        session.commit()
    click.echo(f"Generated {count} employees")
