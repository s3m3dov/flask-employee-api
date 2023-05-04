from http import HTTPStatus as status

from flask.views import MethodView

from app.extensions.api import Blueprint, SQLCursorPage
from app.extensions.database import db
from app.models.employees import Employee
from .schemas import EmployeeSchema

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
    def get(self) -> EmployeeSchema:
        """List employees.

        Returns:
            EmployeeSchema: The list of employees.
        """
        employees = Employee.query.all()
        return employees

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


@blp.route("/<int:employee_id>")
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
        blp.check_etag(employee, EmployeeSchema)
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
        blp.check_etag(employee, EmployeeSchema)
        db.session.delete(employee)
        db.session.commit()
