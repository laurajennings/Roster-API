from main import ma
from marshmallow import fields


class RosterSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("roster_id", "start_date", "shifts")
    shifts = fields.List(fields.Nested("ShiftSchema", exclude=("roster",)))


roster_schema = RosterSchema()

rosters_schema = RosterSchema(many=True)