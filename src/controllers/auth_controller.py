from datetime import timedelta
from flask import Blueprint, jsonify, request
from main import db
from main import bcrypt
from main import jwt 
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.employees import Employee
from schemas.employee_schema import employee_schema
from marshmallow.exceptions import ValidationError

auth = Blueprint('auth', __name__, url_prefix="/auth")

#Add new employee
@auth.route("/register", methods=['POST'])
def register_employee():
    employee_fields = employee_schema.load(request.json)

    employee = Employee.query.filter_by(email=employee_fields["email"]).first()
    if employee:
        return{"error": "email already exists"}

    employee = Employee(
        first_name = employee_fields["first_name"],
        last_name = employee_fields["last_name"],
        email = employee_fields["email"],
        password = bcrypt.generate_password_hash(employee_fields["password"]).decode("utf-8"),
        phone = employee_fields["phone"],
        age = employee_fields["age"],
        pay = employee_fields["pay"]
    )

    db.session.add(employee)
    db.session.commit()
    token = create_access_token(identity=str(employee.employee_id), expires_delta=timedelta(days=1))
    return {"email": employee.email, "token": token}

#Employee login
@auth.route("/login", methods = ['POST'])
def login_employee():
    employee_fields = employee_schema.load(request.json)
    employee = Employee.query.filter_by(email=employee_fields["email"]).first()
    if not employee:
        return {"error": "email is not valid"}
    
    if not bcrypt.check_password_hash(employee.password, employee_fields["password"]):
        return {"error": "password incorrect"}

    token = create_access_token(identity=str(employee.employee_id), expires_delta=timedelta(days=1))

    return {"email": employee.email, "token": token}

#Employee update
@auth.route("/<int:id>", methods=['PUT'])
def update_employee(id):

    employee = Employee.query.get(id)
    if not employee:
        return {"error": "Employee id not found"}
    
    employee_fields = employee_schema.load(request.json)

    employee.first_name = employee_fields["first_name"]
    employee.last_name = employee_fields["last_name"]
    employee.email = employee_fields["email"]
    employee.password = bcrypt.generate_password_hash(employee_fields["password"]).decode("utf-8")
    employee.phone = employee_fields["phone"]
    employee.age = employee_fields["age"]
    employee.pay = employee_fields["pay"]
    
    db.session.commit()
    return jsonify(employee_schema.dump(employee))

#Delete employee
@auth.route("/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}

    #Find employee and delete
    employee = Employee.query.get(id)
    if not employee:
        return {"error": "Employee id not found"}

    db.session.delete(employee)
    db.session.commit()
    return {"message": "Employee has been removed"}

@auth.errorhandler(ValidationError)
def register_validation_error(error):
    return error.messages, 400