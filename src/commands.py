from pickletools import read_int4
from flask import Blueprint
from main import db
from main import bcrypt
from models.rosters import Roster
from models.shifts import Shift
from models.employees import Employee
from models.availability import Availability
from datetime import date, time



db_commands = Blueprint("db", __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables dropped')

@db_commands.cli.command('seed')
def seed_db():
    employee1 = Employee(
        first_name = "Sam",
        last_name = "Jones",
        email = "sam@gmail.com",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
        phone = "04123456789",
        age = "29",
        pay = "25.30",
        manager = True
    )

    db.session.add(employee1)

    employee2 = Employee(
        first_name = "Emily",
        last_name = "Taylor",
        email = "emily@gmail.com",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
        phone = "04123456789",
        age = "17",
        pay = "18.30",
    )

    db.session.add(employee2)

    roster1 = Roster(
        start_date = date(2022, 11, 22)

    )

    db.session.add(roster1)
    db.session.commit()

    shift1 = Shift(
        date = date(2022, 12, 22),
        start_time = time(12, 30, 00),
        end_time = time(18, 30, 00),
        roster_id = roster1.roster_id,
        employee_id = employee1.employee_id
    )
    

    db.session.add(shift1)

    availability1 = Availability(
        day = "Monday",
        start = time(9, 00, 00),
        end = time(15, 00, 00),
        employee = employee1
    )

    db.session.add(availability1)

    db.session.commit()
    print('Tables seeded')