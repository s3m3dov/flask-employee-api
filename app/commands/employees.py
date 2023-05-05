import random
from typing import Optional

import click
import joblib
import pandas as pd
from faker import Faker
from flask import Blueprint
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

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
    department_to_int = {department: i for i, department in enumerate(departments)}
    df["department"] = df["department"].map(department_to_int)
    df["hire_date"] = df["hire_date"].apply(lambda x: x.timestamp())
    click.echo(f"Cleaned up data")

    # Define the columns to be transformed
    categorical_cols = ['department']
    numerical_cols = ['hire_date']

    # Define the transformers
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    # Combine the transformers using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_cols),
            ('num', numerical_transformer, numerical_cols)
        ])

    # Train a model to predict salaries
    # used Ridge regression because it performed better on random data
    # however would use Lasso or MultiLinearRegression for real data
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', Ridge(alpha=1.0))
    ])

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        df[["department", "hire_date"]], df["salary"], test_size=0.25
    )
    click.echo(f"Split data into train and test sets")

    # Fit the model
    model.fit(X_train, y_train)

    # Evaluate the model
    score = model.score(X_test, y_test)
    click.echo(f"Model score: {score}")

    # Save the model
    joblib.dump(model, "model.pkl")
    click.echo(f"Trained model")
