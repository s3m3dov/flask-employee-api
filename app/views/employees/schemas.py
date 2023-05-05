from marshmallow import fields as ma_fields, validates, ValidationError
from marshmallow_sqlalchemy import field_for

from app.constants import departments
from app.extensions.api import AutoSchema, BasePaginatedSchema
from app.models import Employee


class EmployeeSchema(AutoSchema):
    id = field_for(Employee, "id", dump_only=True)

    class Meta(AutoSchema.Meta):
        table = Employee.__table__


class DepartmentSchema(AutoSchema):
    name = ma_fields.Str(required=True)

    @validates("name")
    def validate_department(self, value):
        if value not in departments:
            raise ValidationError(f"{value} is not a valid department")


class EmployeePaginatedSchema(BasePaginatedSchema):
    data = ma_fields.List(ma_fields.Nested(EmployeeSchema()))


class DepartmentPaginatedSchema(BasePaginatedSchema):
    data = ma_fields.List(ma_fields.Nested(DepartmentSchema()))
