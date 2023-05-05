import json
import logging
from datetime import datetime
from http import HTTPStatus as status

import pytest
from faker import Faker
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from app import create_app
from app.constants import departments
from app.extensions.database import db as _db
from app.models import Employee

fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def app():
    _app = create_app()
    ctx = _app.app_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture(scope="session")
def db(app):
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope="session")
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="function")
def session(app, db):
    with app.app_context():
        db.create_all()
        yield db.session
        db.drop_all()


def create_employee(session: Session) -> Employee:
    employee = Employee(
        name=fake.name(),
        hire_date=fake.date_time_between(start_date="-10y", end_date="now"),
        department=fake.random_element(elements=departments),
        salary=fake.random_int(min=30000, max=1000000),
    )
    session.add(employee)
    session.commit()
    return employee


class TestEmployeeEndpoint:
    def test_get_employees(self, client, session):
        employees = [create_employee(session) for i in range(5)]
        response = client.get("/employees/")
        assert response.status_code == status.OK
        assert len(response.json["data"]) == len(employees)

    def test_post_employee(self, client, session):
        data = {
            "name": fake.name(),
            "department": fake.random_element(elements=departments),
            "salary": fake.random_int(min=3000, max=1000000),
            "hire_date": fake.date_time_between(
                start_date="-10y", end_date="now"
            ).strftime("%Y-%m-%d %H:%M:%S"),
        }
        response = client.post("/employees/", json=data, headers={"If-Match": None})
        assert response.status_code == status.CREATED
        assert response.json["name"] == data["name"]

    def test_get_employee_by_id(self, client, session):
        employee = create_employee(session)
        response = client.get(f"/employees/{employee.id}")
        assert response.status_code == status.OK
        assert response.json["name"] == employee.name

    def test_put_employee(self, client, session):
        employee = create_employee(session)
        data = {
            "name": fake.name(),
            "salary": fake.random_int(min=30000, max=1000000),
            "department": fake.random_element(elements=departments),
            "hire_date": fake.date_time_between(
                start_date="-10y", end_date="now"
            ).strftime("%Y-%m-%d %H:%M:%S"),
        }
        response = client.put(f"/employees/{employee.id}", json=data, headers={"If-Match": None})
        assert response.status_code == status.OK
        assert response.json["name"] == data["name"]

    def test_delete_employee(self, client, session):
        employee = create_employee(session)
        response = client.delete(f"/employees/{employee.id}", headers={"If-Match": None})
        assert response.status_code == status.NO_CONTENT
        assert response.data == b""
        assert session.query(Employee).get(employee.id) is None


class TestDepartmentEndpoint:
    def test_get_departments(self, client, session):
        employees = [create_employee(session) for i in range(5)]
        response = client.get("/departments/")
        assert response.status_code == status.OK
        assert len(response.json["data"]) == len(set(e.department for e in employees))

    def test_get_department(self, client, session):
        department = fake.random_element(elements=departments)
        employees = []
        for i in range(5):
            employee = create_employee(session)
            if employee.department == department:
                employees.append(employee)
        response = client.get(f"/departments/{department}")
        assert response.status_code == status.OK
        assert len(response.json["data"]) == len(employees)


class TestStatisticalEndpoint:
    def test_get_average_salary_by_department(self, client, session):
        department = fake.random_element(elements=departments)
        employees = []
        for i in range(5):
            employee = create_employee(session)
            if employee.department == department:
                employees.append(employee)
        response = client.get(f"/average_salary/{department}")
        assert response.status_code == status.OK
        data_1 = response.json.get('data', 0)
        data_2 = sum(e.salary for e in employees) / len(employees) if employees else 0
        assert data_1 == data_2

    def test_get_top_earners(self, client, session):
        employees = [create_employee(session) for i in range(5)]
        response = client.get("/top_earners/")
        assert response.status_code == status.OK
        assert response.json["data"][0]["salary"] == max(e.salary for e in employees)

    def test_get_most_recent_hires(self, client, session):
        employees = [create_employee(session) for i in range(5)]
        response = client.get("/most_recent_hires/")
        assert response.status_code == status.OK
        assert datetime.strptime(
            response.json["data"][0]["hire_date"], "%Y-%m-%dT%H:%M:%S"
        ) == max(e.hire_date for e in employees)

    def test_predict_salary(self, client, session):
        data = {
            "name": "John Doe",
            "department": "Sales",
            "hire_date": datetime(2023, 1, 1).strftime("%Y-%m-%d %H:%M:%S"),
        }
        response = client.post("/predict_salary/", json=data)

        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]

        data = json.loads(response.data)
        assert "data" in data
        assert isinstance(data["data"], float)


"""


def test_post_employee():
    data = {
        "name": fake.name(),
        "email": fake.email(),
        "department": fake.random_element(elements=departments),
        "salary": fake.random_int(min=1000, max=5000),
    }
    response = client.post("/employees/", json=data)
    assert response.status_code == status.CREATED
    assert response.json["name"] == data["name"]


def test_get_employee_by_id():
    employee = create_employee(session)
    response = client.get(f"/employees/{employee.id}")
    assert response.status_code == status.OK
    assert response.json["name"] == employee.name


def test_put_employee(session):
    employee = create_employee(session)
    data = {"name": fake.name(), "salary": fake.random_int(min=1000, max=5000)}
    response = client.put(f"/employees/{employee.id}", json=data)
    assert response.status_code == status.OK
    assert response.json["name"] == data["name"]


def test_delete_employee(session):
    employee = create_employee(session)
    response = client.delete(f"/employees/{employee.id}")
    assert response.status_code == status.NO_CONTENT
    assert session.query(Employee).filter_by(id=employee.id).first() is None


def test_get_departments(session):
    employees = [create_employee(session) for i in range(5)]
    response = client.get("/departments/")
    assert response.status_code == status.OK
    assert len(response.json["data"]["items"]) == len(
        set(e.department for e in employees)
    )


def test_get_department(session):
    department = fake.random_element(elements=departments)
    employees = []
    for i in range(5):
        employee = create_employee(session)
        employees.append(employee)

    session.commit()
    response = client.get(f"/departments/{department}")
    assert response.status_code == status.OK
    assert len(response.json["data"]["items"]) == len(employees)


def test_average_salary():
    response = client.get("/api/v1/average_salary/HR")

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    data = json.loads(response.data)
    assert "data" in data
    assert isinstance(data["data"], float)


def test_top_earners():
    response = client.get("/api/v1/top_earners/")

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    data = json.loads(response.data)
    assert "data" in data
    assert "pagination" in data
    assert isinstance(data["data"]["items"], list)
    assert len(data["data"]["items"]) == 10


def test_most_recent_hires():
    response = client.get("/api/v1/most_recent_hires/")

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    data = json.loads(response.data)
    assert "data" in data
    assert "pagination" in data
    assert isinstance(data["data"]["items"], list)


def test_predict_salary():
    data = {
        "department": "Sales",
        "hire_date": datetime(2023, 1, 1),
        "job_title": "Sales Representative",
    }
    response = client.post("/api/v1/predict_salary/", json=data)

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    data = json.loads(response.data)
    assert "data" in data
    assert isinstance(data["data"], float)
"""
