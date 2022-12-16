from main import ma
from marshmallow import fields

class ShiftSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["employee", "shift_id", "date", "start_time", "end_time", "roster_id", "roster", "employee_id"]
        load_only = ['roster_id', 'employee_id', "shift_id"]
    roster = fields.Nested("RosterSchema", exclude=("shifts", "roster_id"))
    employee = fields.Nested("EmployeeSchema", only=("first_name", "last_name"))

shift_schema = ShiftSchema()
shifts_schema = ShiftSchema(many=True)