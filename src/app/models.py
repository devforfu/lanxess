from calendar import day_name

from sqlalchemy.dialects.postgresql import ENUM

from . import db


TIMESLOT_DURATION = 15
MINUTES_PER_HOUR = 60

days_of_week = tuple(day_name)
hours = [str(x) for x in range(24)]
minutes_granularity = [str(x) for x in range(0, 60, TIMESLOT_DURATION)]

days_of_week_enum = ENUM(*days_of_week, name='days_of_week')
hours_enum = ENUM(*hours, name='hours')
minutes_enum = ENUM(*minutes_granularity, name='minutes')


employee_timeslots = db.Table(
    'employee_timeslots',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id')),
    db.Column('timeslots_id', db.Integer, db.ForeignKey('timeslots.id')))


candidate_timeslots = db.Table(
    'candidate_timeslots',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidates.id')),
    db.Column('timeslots_id', db.Integer, db.ForeignKey('timeslots.id')))


class PersonMixin:
    """Common computed properties and methods for employees and candidates."""

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def exists(first_name, last_name):
        employee = Employee.query.filter_by(
            first_name=first_name, last_name=last_name).first()
        return employee is not None


class Employee(PersonMixin, db.Model):
    """Company's employee responsible for carrying out interviews."""

    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    availability = db.relationship('Timeslot', secondary=employee_timeslots)
    interviews = db.relationship('Interview',
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
    availability = db.relationship('Timeslot', secondary=candidate_timeslots)


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

    @property
    def verbose_start(self):
        start = self.start
        verbose = f'On {start.day} at {int(start.hour):02d}:{int(start.minute):02d}'
        return verbose

    @property
    def verbose_duration(self):
        minutes = TIMESLOT_DURATION * self.duration_in_timeslots
        whole_hours = minutes // MINUTES_PER_HOUR
        rest_of_minutes = minutes - (hours * MINUTES_PER_HOUR)
        return f'{whole_hours}h {rest_of_minutes}m'


def entity_with_id(entity_cls, id_value):
    return entity_cls.query.filter_by(id=id_value).first()
