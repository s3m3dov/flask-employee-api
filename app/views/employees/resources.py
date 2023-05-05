import logging
from http import HTTPStatus as status

import joblib
import pandas as pd
import sqlalchemy as sa
from flask import request, current_app
from flask.views import MethodView

from app.extensions.api import Blueprint
from app.extensions.database import db
from app.models.employees import Employee
from app.utils.pagination import get_pagination
from .schemas import (
    EmployeeSchema,
    DepartmentSchema,
    DepartmentPaginatedSchema,
    EmployeePaginatedSchema,
    AverageSalarySchema,
    SalaryPredictedSchema,
    SalaryPredictInputSchema,
)
from app.constants import departments

blp = Blueprint(
    "Employees",
    __name__,
    url_prefix="/",
    description="Operations on employees, departments, and salaries",
)

# Load the trained model.
model = joblib.load("model.pkl")
# Logger
logger = logging.getLogger(__name__)


@blp.route("/employees/")
class Employees(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=EmployeePaginatedSchema)
    def get(self) -> dict:
        """List employees.

        Returns:
            EmployeeSchema: The list of employees.
        """
        page = request.args.get("page", 1, type=int)
        per_page = current_app.config.get("PER_PAGE_LIMIT")
        logger.debug(f"page: {page}, per_page: {per_page}")

        employees = Employee.query.paginate(
            page=page, per_page=per_page, error_out=True
        )
        pagination = get_pagination(employees)
        return {"data": employees, "pagination": pagination}

    @blp.etag
    @blp.arguments(EmployeeSchema)
    @blp.response(status_code=status.CREATED, schema=EmployeeSchema)
    def post(self, data: EmployeeSchema) -> EmployeeSchema:
        """Create a new employee.
        Args:
            data: EmployeeSchema: The data to use to create the employee.

        Returns:
            EmployeeSchema: The created employee.
        """
        employee = Employee(**data)
        db.session.add(employee)
        db.session.commit()
        return employee


@blp.route("/employees/<int:employee_id>")
class EmployeeById(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=EmployeeSchema)
    def get(self, employee_id: int) -> EmployeeSchema:
        """Get an employee.
        Args:
            employee_id: int: The ID of the employee to get.

        Returns:
            EmployeeSchema: The employee.
        """
        employee = Employee.query.get_or_404(employee_id)
        return employee

    @blp.etag
    @blp.arguments(EmployeeSchema)
    @blp.response(status_code=status.OK, schema=EmployeeSchema)
    def put(self, data: EmployeeSchema, employee_id: int) -> EmployeeSchema:
        """Update an existing employee.
        Args:
            data: EmployeeSchema: The data to use to update the employee.
            employee_id: int: The ID of the employee to update.

        Returns:
            EmployeeSchema: The updated employee.
        """
        employee = Employee.query.get_or_404(employee_id)
        logger.debug(employee_id)
        EmployeeSchema().update(employee, data)
        db.session.add(employee)
        db.session.commit()
        return employee

    @blp.etag
    @blp.response(status_code=status.NO_CONTENT)
    def delete(self, employee_id: int) -> None:
        """Delete an employee.
        Args:
            employee_id: int: The ID of the employee to delete.
        """
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()


@blp.route("/departments/")
class Departments(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=DepartmentPaginatedSchema)
    def get(self) -> dict:
        """List departments.

        Returns:
            DepartmentSchema: The list of departments.
        """
        page = request.args.get("page", 1, type=int)
        per_page = current_app.config.get("PER_PAGE_LIMIT")
        logger.debug(f"page: {page}, per_page: {per_page}")

        departments = (
            Employee.query.distinct(Employee.department)
            .with_entities(Employee.department.label("name"))
            .paginate(page=page, per_page=per_page, error_out=True)
        )
        pagination = get_pagination(departments)
        return {"data": departments, "pagination": pagination}


@blp.route("/departments/<string:department>")
class Department(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=EmployeePaginatedSchema)
    def get(self, department: str) -> dict:
        """Get employees of a department.
        Args:
            department: str: The name of the department to get employees for.

        Returns:
            EmployeeSchema: The list of employees for the department.
        """
        logger.debug(f"department: {department}")
        department = DepartmentSchema().load({"name": department})

        page = request.args.get("page", 1, type=int)
        per_page = current_app.config.get("PER_PAGE_LIMIT")
        logger.debug(f"page: {page}, per_page: {per_page}")

        employees = (
            Employee.query.filter_by(department=department["name"])
            .order_by(Employee.hire_date.desc())
            .paginate(page=page, per_page=per_page, error_out=True)
        )

        pagination = get_pagination(employees)
        return {"data": employees, "pagination": pagination}


@blp.route("/average_salary/<string:department>")
class AverageSalary(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=AverageSalarySchema)
    def get(self, department: str) -> dict:
        """Get the average salary of employees in the specified department.

        Args:
            department: str: The name of the department to get the average salary for.

        Returns:
            int: average salary.
        """
        logger.debug(f"department: {department}")
        department = DepartmentSchema().load({"name": department})
        avg_salary = (
            Employee.query.with_entities(sa.func.avg(Employee.salary))
            .filter_by(department=department["name"])
            .scalar()
        )
        logger.debug(f"avg_salary: {avg_salary}")
        return {"data": avg_salary}


@blp.route("/top_earners/")
class TopEarners(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=EmployeePaginatedSchema)
    def get(self) -> dict:
        """Get a list of the top 10 earners in the company based on their salary.

        Returns:
            EmployeeSchema: A list of the top 10 earners in the company.
        """
        page = request.args.get("page", 1, type=int)
        per_page = current_app.config.get("PER_PAGE_LIMIT")
        top_result_limit = current_app.config.get("TOP_RESULT_LIMIT")

        logger.debug(
            f"page: {page}, per_page: {per_page}, top_result_limit: {top_result_limit}"
        )

        top_employees_cte = (
            db.session.query(Employee)
            .order_by(Employee.salary.desc())
            .limit(top_result_limit)
            .cte()
        )
        employees = db.session.query(top_employees_cte).paginate(
            page=page, per_page=per_page, error_out=True
        )

        logger.debug(employees)
        pagination = get_pagination(employees)
        return {"data": employees, "pagination": pagination}


@blp.route("/most_recent_hires/")
class MostRecentHires(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=EmployeePaginatedSchema)
    def get(self) -> dict:
        """Get a list of the most recent hires in the company.

        Returns:
            EmployeeSchema: A list of the most recent hires in the company.
        """
        page = request.args.get("page", 1, type=int)
        per_page = current_app.config.get("PER_PAGE_LIMIT")
        top_result_limit = current_app.config.get("TOP_RESULT_LIMIT")

        logger.debug(
            f"page: {page}, per_page: {per_page}, top_result_limit: {top_result_limit}"
        )

        top_employees_cte = (
            db.session.query(Employee)
            .order_by(Employee.hire_date.desc())
            .limit(top_result_limit)
            .cte()
        )
        employees = db.session.query(top_employees_cte).paginate(
            page=page, per_page=per_page, error_out=True
        )

        logger.debug(employees)
        pagination = get_pagination(employees)
        return {"data": employees, "pagination": pagination}


@blp.route("/predict_salary/")
class PredictSalary(MethodView):
    @blp.etag
    @blp.arguments(EmployeeSchema)
    @blp.response(status_code=status.OK, schema=SalaryPredictedSchema)
    def post(self, data: SalaryPredictInputSchema) -> dict:
        """Predict the salary of a new employee based on department, hire date, and job title

        Args:
            data: EmployeeSchema: The data to use to predict the salary of the employee.

        Returns:
            int: predicted salary.
        """
        logger.debug(f"data: {data}")
        data = {
            "department": data["department"],
            "hire_date": data["hire_date"].timestamp(),
        }
        # Convert the data to a Pandas DataFrame.
        df = pd.DataFrame(data, index=[0])
        department_to_int = {department: i for i, department in enumerate(departments)}
        df["department"] = df["department"].map(department_to_int)

        # Predict the salary.
        prediction = model.predict(df)

        # Return the prediction.
        return {"data": prediction}
