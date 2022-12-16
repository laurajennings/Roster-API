from main import db

class Employee(db.Model):
    __tablename__="employees"
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    pay = db.Column(db.Float(), nullable=False)
    manager = db.Column(db.Boolean(), default = False)
    availability = db.relationship(
        "Availability",
        backref = "employee",
        cascade="all, delete"
    )
    shifts = db.relationship(
        "Shift",
        backref="employee",
        cascade="all, delete"
    )