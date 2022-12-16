from main import db

class Roster(db.Model):
    __tablename__="rosters"
    roster_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    shifts = db.relationship(
        "Shift",
        backref="roster"
    )
