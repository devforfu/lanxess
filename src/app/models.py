from calendar import day_name

from sqlalchemy.dialects.postgresql import ENUM

from . import db


days_of_week = tuple(day_name)
hours = [str(x) for x in range(24)]
minutes_granularity = [str(x) for x in  (0, 15, 30, 45)]

days_of_week_enum = ENUM(*days_of_week, name='days_of_week')
hours_enum = ENUM(*hours, name='hours')
minutes_enum = ENUM(*minutes_granularity, name='minutes')


class Employee(db.Model):
    """Company's employee responsible for carrying out interviews."""

    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    availability = db.relationship('EmployeeTimeslot',
                                   uselist=True,
                                   backref='employee',
                                   passive_deletes='all')

class Candidate(db.Model):
    """Interviewed candidate."""

    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    skype = db.Column(db.String(64), default=None)
    email = db.Column(db.String(254), nullable=False)
    availability = db.relationship('CandidateTimeslot',
                                   uselist=True,
                                   backref='candidate',
                                   passive_deletes='all')


class EmployeeTimeslot(db.Model):
    """Interviewer's free timeslots."""

    __tablename__ = 'employees_timeslots'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(
        db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    timeslot_id = db.Column(
        db.Integer, db.ForeignKey('timeslots.id'))


class CandidateTimeslot(db.Model):
    """Candidate's free timeslots."""

    __tablename__ = 'candidates_timeslots'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(
        db.Integer, db.ForeignKey('candidates.id', ondelete='CASCADE'))
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'))


class Timeslot(db.Model):
    """Entity representing discrete availability timeslot."""

    __tablename__ = 'timeslots'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(days_of_week_enum, nullable=False)
    hour = db.Column(hours_enum, nullable=False)
    minute = db.Column(minutes_enum, nullable=False)


class Interview(db.Model):
    """The list of allocated interviews."""

    __tablename__ = 'interviews'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('employees.id', ondelete='CASCADE'),
        nullable=False)
    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey('candidates.id', ondelete='CASCADE'),
        nullable=False)
    start = db.Column(db.Integer, db.ForeignKey('timeslots.id'), nullable=False)
    duration_in_timeslots = db.Column(db.Integer, nullable=False)
