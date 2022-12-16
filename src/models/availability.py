from main import db
import datetime

class Availability(db.Model):
    __tablename__ = "availability"

    availability_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String())
    start = db.Column(db.Time())
    end = db.Column(db.Time())
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_id"), nullable=False)