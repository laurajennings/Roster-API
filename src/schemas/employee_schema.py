from main import ma
from marshmallow.validate import Length

class EmployeeSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ["employee_id", "first_name", "last_name", "email", "password", "phone", "age", "pay", "manager"]

    password = ma.String(validate=Length(min=8))
    username = ma.String(required = True) 
    email = ma.String(required = True) 
    
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)