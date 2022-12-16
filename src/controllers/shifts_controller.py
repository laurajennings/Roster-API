from flask import Blueprint, jsonify, request
from main import db
from models.shifts import Shift
from models.employees import Employee
from schemas.shift_schema import shift_schema, shifts_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

shifts = Blueprint('shifts', __name__, url_prefix="/shifts")

#Show shifts
@shifts.route("/", methods=['GET'])
@jwt_required()
def get_shifts():

    shifts_list = Shift.query.all()
    result = shifts_schema.dump(shifts_list)
    return jsonify(result)

#Show specific shift
@shifts.route("/<int:id>", methods=['GET'])
@jwt_required()
def get_shift(id):

    shift = Shift.query.get(id)
    if not shift:
        return {"error": "Shift id not found"}

    shift = Shift.query.get(id)
    result = shift_schema.dump(shift)
    return jsonify(result)

#Add shift
@shifts.route("/", methods=['POST'])
@jwt_required()
def new_shift():
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}

    shift_fields = shift_schema.load(request.json)
    shift = Shift(
        date = shift_fields["date"],
        start_time = shift_fields["start_time"],
        end_time = shift_fields["end_time"],
        roster_id = shift_fields["roster_id"],
        employee_id = shift_fields["employee_id"]
    )
    
    db.session.add(shift)
    db.session.commit()
    return jsonify(shift_schema.dump(shift))

#Update shift
@shifts.route("/<int:id>", methods=['PUT'])
@jwt_required()
def update_shift(id):
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}
    
    #Finds and updates shift
    shift = Shift.query.get(id)
    if not shift:
        return {"error": "Shift id not found"}
    
    shift_fields = shift_schema.load(request.json)

    shift.date = shift_fields["date"]
    shift.start_time = shift_fields["start_time"]
    shift.end_time = shift_fields["end_time"]

    db.session.commit()
    return jsonify(shift_schema.dump(shift))

#Delete shift
@shifts.route("/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_shift(id):
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}

    #Find employee
    shift = Shift.query.get(id)
    if not shift:
        return {"error": "Shift id not found"}

    db.session.delete(shift)
    db.session.commit()
    return {"message": "Shift has been removed"}