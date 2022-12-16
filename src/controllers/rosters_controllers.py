from flask import Blueprint, jsonify, request
from main import db
from models.rosters import Roster
from models.employees import Employee
from schemas.roster_schema import roster_schema, rosters_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

rosters = Blueprint('rosters', __name__, url_prefix="/rosters")

#Show all rosters
@rosters.route("/", methods=['GET'])
def get_rosters():
    rosters_list = Roster.query.all()
    result = rosters_schema.dump(rosters_list)
    return jsonify(result)

#Show specific roster
@rosters.route("/<int:id>", methods=['GET'])
def get_roster(id):
    roster = Roster.query.get(id)
    if not roster: 
        return {"error": "roster id not found"}
    result = roster_schema.dump(roster)
    return jsonify(result)

#Add new roster
@rosters.route("/", methods=['POST'])
@jwt_required()
def create_roster():
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}

    roster_fields = roster_schema.load(request.json)
    roster = Roster(
        start_date = roster_fields["start_date"]
    )

    db.session.add(roster)
    db.session.commit()

    return jsonify(roster_schema.dump(roster))

#Update roster
@rosters.route("/<int:id>", methods=['PUT'])
@jwt_required()
def update_roster(id):
    #Checks manager identity
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}
    
    #Finds and updates shift
    roster = Roster.query.get(id)
    if not roster:
        return {"error": "Roster id not found"}
    
    roster_fields = roster_schema.load(request.json)

    roster.start_date = roster_fields["start_date"]

    db.session.commit()
    return jsonify(roster_schema.dump(roster))

#Delete roster
@rosters.route("<int:id>", methods=['DELETE'])
@jwt_required()
def delete_roster(id):
    employee_id = get_jwt_identity()
    employee = Employee.query.get(employee_id)
    if not employee.manager:
        return {"error": "Not authorized"}

    roster = Roster.query.get(id)
    if not roster:
        return {"error": "roster id not found"}

    db.session.delete(roster)
    db.session.commit()
    return {"message": "Roster has been removed"}