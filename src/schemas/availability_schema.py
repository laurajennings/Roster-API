from main import ma
from marshmallow import fields

class AvailabilitySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ( "availability_id", "employee", "day", "start", "end", "employee_id")
        load_only = ['employee_id']
    employee = fields.Nested("EmployeeSchema", only=("first_name", "last_name"))
availability_schema = AvailabilitySchema()
availabilities_schema = AvailabilitySchema(many=True)