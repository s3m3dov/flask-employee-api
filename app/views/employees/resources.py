from http import HTTPStatus as status

from flask import request
from flask.views import MethodView

from app.extensions.api import Blueprint, SQLCursorPage
from app.extensions.database import db
from app.models.employees import Employee
from .schemas import EmployeeSchema

# Create the API blueprint
blp = Blueprint(
    "Employees",
    __name__,
    url_prefix="/employees",
    description="Operations on employees",
)


@blp.route("/")
class Employees(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=EmployeeSchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self):
        """List all employees."""
        employees = Employee.query.all()
        return EmployeeSchema(many=True).dump(employees)

    @blp.etag
    @blp.arguments(EmployeeSchema)
    @blp.response(status_code=status.CREATED, schema=EmployeeSchema)
    def post(self):
        """Create a new employee."""
        data = request.get_json()
        employee = Employee(**data)
        db.session.add(employee)
        db.session.commit()
        return EmployeeSchema().dump(employee)


@blp.route("/<int:employee_id>")
class EmployeeById(MethodView):
    @blp.etag
    @blp.response(status_code=status.OK, schema=EmployeeSchema)
    def get(self, employee_id):
        """Get an employee by ID."""
        employee = Employee.query.get_or_404(employee_id)
        return EmployeeSchema().dump(employee)

    @blp.etag
    @blp.arguments(EmployeeSchema)
    @blp.response(status_code=status.OK, schema=EmployeeSchema)
    def put(self, employee_id):
        """Update an existing employee."""
        data = request.get_json()
        employee = Employee.query.get_or_404(employee_id)
        EmployeeSchema().update(employee, data)
        db.session.commit()
        return EmployeeSchema().dump(employee)

    @blp.etag
    @blp.response(status_code=status.NO_CONTENT)
    def delete(self, employee_id):
        """Delete an employee."""
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return "", status.NO_CONTENT
