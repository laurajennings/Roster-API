from controllers.employees_controller import employees
from controllers.shifts_controller import shifts
from controllers.rosters_controllers import rosters
from controllers.auth_controller import auth

registerable_controllers = [shifts, employees, rosters, auth]