import random
from typing import Optional

import click
import joblib
import pandas as pd
from faker import Faker
from flask import Blueprint
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

from app.constants import departments
from app.extensions.database import db
from app.models.employees import Employee

blp = Blueprint("employees", __name__, cli_group=None)


@blp.cli.command("generate-employees")
@click.option("--count", default=100, help="Number of employees to generate")
def generate_employees(count: Optional[int] = 100):
    """Generate random employees

    Args:
        count (int, optional): Number of employees to generate. Defaults to 100.
    """
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


@blp.cli.command("train-salary-model")
def train_salary_prediction_model():
    """Train a model to predict salaries"""

    # Load the fetched data into a Pandas DataFrame
    engine = db.engine
    df = pd.read_sql_table(table_name="employees", con=engine)
    df.drop(columns=["id", "name"], inplace=True)
    click.echo(f"Loaded {len(df)} employees, columns: {df.columns}")

    # Clean up the data
    df["department"] = df["department"].factorize()[0]
    df["hire_date"] = df["hire_date"].apply(lambda x: x.timestamp())
    click.echo(f"Cleaned up data")

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        df[["department", "hire_date"]], df["salary"], test_size=0.25
    )
    click.echo(f"Split data into train and test sets")

    # Train a model to predict salaries
    #
    model = Ridge(alpha=0.1)
    model.fit(X_train, y_train)

    # Evaluate the model
    score = model.score(X_test, y_test)
    click.echo(f"Model score: {score}")

    # Save the model
    joblib.dump(model, "model.pkl")
    click.echo(f"Trained model")
