from marshmallow_sqlalchemy import field_for

from app.extensions.api import AutoSchema
from app.models import Employee


class EmployeeSchema(AutoSchema):
    id = field_for(Employee, "id", dump_only=True)

    class Meta(AutoSchema.Meta):
        table = Employee.__table__
