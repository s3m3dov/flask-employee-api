"""Members schema"""

import marshmallow as ma
from marshmallow_sqlalchemy import field_for

from app.extensions.api import Schema, AutoSchema
from app.models import Member


class MemberSchema(AutoSchema):
    id = field_for(Member, "id", dump_only=True)

    class Meta(AutoSchema.Meta):
        table = Member.__table__


class MemberQueryArgsSchema(Schema):
    first_name = ma.fields.Str()
    last_name = ma.fields.Str()
    team_id = ma.fields.UUID()
