from . import db


class Employee(db.Model):
    """Company's employee responsible for carrying out interviews."""

    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)


class Candidate(db.Model):
    """Interviewed candidate."""

    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    skype = db.Column(db.String(64), default=None)
    email = db.Column(db.String(254), nullable=False)


class EmployeeTimeslot(db.Model):
    """Timeslots to represent employee's free time."""

    __tablename__ = 'employees_timeslots'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(
        db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)


class CandidateTimeslot(db.Model):
    """Timeslots to represent candidate's free time."""

    __tablename__ = 'candidates_timeslots'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(
        db.Integer, db.ForeignKey('candidates.id', ondelete='CASCADE'))
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)
