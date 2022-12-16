from flask import Blueprint, jsonify, request
from main import db
from models.employees import Employee
from models.availability import Availability
from schemas.employee_schema import employee_schema, employees_schema
from schemas.availability_schema import availability_schema, availabilities_schema
from flask_jwt_extended import jwt_required, get_jwt_identity


employees = Blueprint('employees', __name__, url_prefix="/employees")

@employees.route("/", methods=['GET'])
@jwt_required()
def get_employees():
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}

    #Shows all employees    
    employees_list = Employee.query.all()
    result = employees_schema.dump(employees_list)
    return jsonify(result)

@employees.route("/<int:id>", methods=['GET'])
@jwt_required()
def get_employee(id):
        #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}

    #Shows individual employee
    employee = Employee.query.get(id)
    if not employee: 
        return {"error": "Employee id not found"}
    result = employee_schema.dump(employee)
    return jsonify(result)



#AVAILABILITIES
#Show availabilities
@employees.route("/availability", methods=['GET'])
@jwt_required()
def get_all_availabilities():
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}
    
    #Filters by day
    if request.query_string:
        if request.args.get('day'):
            filtered_availability_list = Availability.query.filter_by(day= request.args.get('day'))
            result = availabilities_schema.dump(filtered_availability_list)
            return jsonify(result)
    #Filters by employee_id
        if request.args.get('employee_id'):
            filtered_availability_list = Availability.query.filter_by(employee_id= request.args.get('employee_id'))
            result = availabilities_schema.dump(filtered_availability_list)
            return jsonify(result)
    #Shows all availabilities
    availabilities_list = Availability.query.all()
    result = availabilities_schema.dump(availabilities_list)
    return jsonify(result)

#New Availability
@employees.route("/availability", methods=['POST'])
@jwt_required()
def new_availability():
    #Get identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Not authorized"}


    availability_fields = availability_schema.load(request.json)
    availability = Availability(
        employee = employee,
        day = availability_fields["day"],
        start = availability_fields["start"],
        end = availability_fields["end"]
    )

    db.session.add(availability)
    db.session.commit()
    return jsonify(availability_schema.dump(availability))

@employees.route("/availability/<int:id>", methods=['PUT'])
@jwt_required()
def update_availability(id):
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Not authorized"}

    #Finds and updates shift
    availability = Availability.query.get(id)
    if not availability:
        return {"error": "Availibility id not found"}
    
    availability_fields = availability_schema.load(request.json)

    availability.day = availability_fields["day"]
    availability.start = availability_fields["start"]
    availability.end = availability_fields["end"]

    db.session.commit()
    return jsonify(availability_schema.dump(availability))

@employees.route("/availability/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_availability(id):
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Not authorized"}

    #Find availability and delete
    availability = Availability.query.get(id)
    if not availability:
        return {"error": "Availability id not found"}

    db.session.delete(availability)
    db.session.commit()
    return {"message": "Employee has been removed"}