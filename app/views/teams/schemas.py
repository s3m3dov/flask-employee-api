"""Teams schema"""

import marshmallow as ma
from marshmallow_sqlalchemy import field_for

from app.extensions.api import Schema, AutoSchema
from app.models import Team


class TeamSchema(AutoSchema):
    id = field_for(Team, "id", dump_only=True)

    class Meta(AutoSchema.Meta):
        table = Team.__table__


class TeamQueryArgsSchema(Schema):
    name = ma.fields.Str()
    member_id = ma.fields.UUID()
