from main import db

class Shift(db.Model):
    __tablename__="shifts"
    shift_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    roster_id = db.Column(db.Integer, db.ForeignKey("rosters.roster_id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_id"), nullable=False)