"""
Interviews management API.
"""
import re
from collections import namedtuple

from flask import jsonify, request, current_app
from werkzeug.exceptions import HTTPException

from . import main
from .. import db
from ..models import days_of_week, TIMESLOT_DURATION
from ..models import Employee, Candidate, Timeslot
from ..models import entity_with_id


@main.route('/api/v1/echo', methods=['GET'])
def echo():
    """Dummy endpoint to test app's setup."""
    return jsonify({'success': True})


@main.route('/api/v1/employee', methods=['GET', 'POST', 'DELETE'])
def employee_endpoint():
    """
    Manages employees responsible to carry out interviews.

    Required parameters:
        * first_name (str): The first name of employee.
        * last_name (str): The last name of employee.

    """
    ok, result = _get_json_keys('first_name', 'last_name')
    if not ok:
        return result.error

    payload = result.payload

    if request.method == 'GET':
        employee = Employee.query.filter_by(**payload).first()
        if employee is None:
            return api_bad_request(f'employee is not found')

        interviews_records = [{
            'start': {
                'day': interview.start.day,
                'hour': interview.start.hour,
                'minute': interview.start.minute},
            'start_verbose': interview.verbose_start,
            'duration_in_minutes': interview.duration_in_minutes,
            'duration_verbose': interview.verbose_duration
            } for interview in employee.interviews]

        payload['interviews'] = interviews_records
        return success(payload)

    elif request.method == 'POST':
        if Employee.exists(**payload):
            return api_bad_request('cannot create employee: the record already exist')

        employee = Employee(**payload)
        db.session.add(employee)
        db.session.commit()
        return success({'id': employee.id})

    elif request.method == 'DELETE':
        employee = Employee.query.filter_by(**payload).first()
        if employee is None:
            return api_bad_request('cannot delete non-existing employee')

        db.session.delete(employee)
        db.session.commit()
        return success({'id': employee.id})


@main.route('/api/v1/candidate', methods=['GET', 'POST', 'DELETE'])
def candidate_endpoint():
    """
    Manages employees responsible to carry out interviews.

    Required parameters:
        * first_name (str): The first name of employee.
        * last_name (str): The last name of employee.

    POST-specific parameters:
        * email (str): Candidate's email
        * skype (str): Candidate's Skype

    """
    ok, result = _get_json_keys('first_name', 'last_name')
    if not ok:
        return result.error

    payload = result.payload

    if request.method == 'GET':
        candidate = Candidate.query.filter_by(**payload).first()
        if candidate is None:
            return api_bad_request(f'candidate is not found')

        record = payload.copy()
        record['email'] = candidate.email
        record['skype'] = candidate.skype or ''

        if candidate.interview is not None:
            interview_obj = candidate.interview
            interview = {
                'start': {
                    'day': interview_obj.start.day,
                    'hour': interview_obj.start.hour,
                    'minute': interview_obj.start.minute},
                'start_verbose': interview_obj.verbose_start,
                'duration_in_minutes': interview_obj.duration_in_minutes,
                'duration_verbose': interview_obj.verbose_duration}
            record['interview'] = interview

        return success(record)

    elif request.method == 'POST':
        if Candidate.exists(**payload):
            return api_bad_request('cannot create candidate: the record already exist')

        email = request.json.get('email')
        if email is None:
            return api_bad_request('cannot create candidate without email')

        payload['email'] = email
        payload['skype'] = request.json.get('skype')
        candidate = Candidate(**payload)
        db.session.add(candidate)
        db.session.commit()
        return success({'id': candidate.id})

    elif request.method == 'DELETE':
        candidate = Candidate.query.filter_by(**payload).first()
        if candidate is None:
            return api_bad_request('cannot delete non-existing candidate')

        db.session.delete(candidate)
        db.session.commit()
        return success({'id': candidate.id})


@main.route('/api/v1/allocate_employee_time', methods=['POST'])
def allocate_employee_time():
    """
    Allocates free timeslots for interview for employee or candidate.

    Required parameters:
        * employee_id (int): An ID of employee to allocate time.
        * day (str): An interview day.
        * time (str): Time value in format 'hh:mm', converted to the closest discrete timeslot.

    """
    req = TimeAllocationRequest(request, ('employee_id', 'day', 'time'))
    if not req.validate():
        return req.error

    timeslot = req.create_or_query_timeslot()
    employee_id = req.parsed('employee_id')
    employee = entity_with_id(Employee, employee_id)
    if employee is None:
        return api_bad_request('employee ID=%d does not exist' % employee_id)

    if timeslot not in employee.availability:
        employee.availability.append(timeslot)

    return _create_availability_response(employee)


@main.route('/api/v1/allocate_candidate_time', methods=['POST'])
def allocate_candidate_time():
    return api_bad_request('not implemented')


@main.route('/api/v1/list_interviews', methods=['GET'])
def list_interviews():
    """
    Returns list of available interview timeslots for a specific candidate and a given
    list of interviewers.

    Required parameters:
        * candidate (int): An ID of interviewed candidate.
        * employees (list): A list of employees considered to carry out interview.

    """
    keys = 'candidate', 'employees'
    ok, result = _get_json_keys(*keys)
    if not ok:
        return result.error

    candidate_id, employees_list = _unwrap(keys, result.payload)
    candidate = entity_with_id(Candidate, candidate_id)
    if candidate is None:
        return api_bad_request('candidate with ID=%d is not found' % candidate_id)

    employees = Employee.query.filter(Employee.id.in_(employees_list))
    schedule = []
    for employee in employees:
        common_timeslots = [
            ts for ts in employee.availability if ts in candidate.availability]
        if not common_timeslots:
            continue
        for timeslot in common_timeslots:
            record = {
                'interviewer': employee.full_name,
                'day': timeslot.day,
                'hour': timeslot.hour,
                'minute': timeslot.minute}
            schedule.append(record)

    if not schedule:
        return api_bad_request('no available timeslots')

    return success({'schedule': schedule})


@main.route('/api/v1/interview', methods=['GET', 'POST', 'DELETE'])
def interview_endpoint():
    return api_bad_request('not implemented')


class TimeAllocationRequest:
    """
    Helper class to parse time allocation request parameters and return new or existing
    timeslot object to be included into person's availability list.
    """

    def __init__(self, request_obj, expected_keys, time_regex='^(\d\d)?:(\d\d)?$'):
        self.request_obj = request_obj
        self.expected_keys = expected_keys
        self.time_regex = time_regex
        self._error = None
        self._params = None
        self._parsed = None

    @property
    def error(self):
        return self._error

    def parsed(self, value):
        if value not in self._parsed:
            raise KeyError('unknown request parameter: %s' % value)
        return self._parsed[value]

    def validate(self):
        ok, result = _get_json_keys(*self.expected_keys)

        if not ok:
            self._error = result.error
            return False

        person_id, day, time = _unwrap(self.expected_keys, result.payload)

        if day not in days_of_week:
            self._error = api_bad_request('invalid day of weeK: %s' % day)
            return False

        match = re.match(self.time_regex, time)
        if match is None:
            self._error = api_bad_request('invalid time format')
            return False

        hour, minute = [int(x) for x in match.groups()]
        if not (0 <= hour < 23) or not (0 <= minute <= 59):
            self._error = api_bad_request('time out of range')
            return False

        minute_rounded = TIMESLOT_DURATION * (minute // TIMESLOT_DURATION)
        params = dict(day=day, hour=str(hour), minute=str(minute_rounded))
        self._params = params
        self._parsed = result.payload
        return True

    def create_or_query_timeslot(self):
        timeslot = Timeslot.query.filter_by(**self._params).first()
        if timeslot is None:
            timeslot = Timeslot(**self._params)
            db.session.add(timeslot)
            db.session.commit()
        return timeslot


def success(data=None):
    data = data or {}
    data['success'] = True
    return jsonify(data)


def error(error_name, error_description=None, data=None):
    data = data or {}
    data['success'] = False
    data['error'] = error_name
    if error_description:
        data['message'] = error_description
    return jsonify(data)


def api_bad_request(message):
    response = error('bad request', message)
    response.status_code = 400
    return response


def api_unauthorized(message):
    response = error('unauthorized', message)
    response.status_code = 401
    return response


def api_forbidden(message):
    response = error('forbidden', message)
    response.status_code = 403
    return response


def api_resource_not_found(message):
    response = error('resource not found', message)
    response.status_code = 404
    return response


@main.app_errorhandler(400)
def bad_request(e):
    response = error('bad request')
    response.status_code = 400
    return response


@main.app_errorhandler(403)
def forbidden(e):
    response = error('forbidden')
    response.status_code = 403
    return response


@main.app_errorhandler(404)
def not_found(e):
    response = error('endpoint not found')
    response.status_code = 404
    return response


@main.app_errorhandler(405)
def method_not_allowed(e):
    response = error('method not allowed')
    response.status_code = 405
    return response


@main.app_errorhandler(Exception)
def rest_of_errors(e):
    current_app.custom_logger.error('Server error occurred')
    current_app.custom_logger.error(str(e))
    response = error('unexpected server error')
    response.status_code = e.code if isinstance(e, HTTPException) else 500
    return response


def _get_json_keys(key, *keys):
    keys = [key] + list(keys)
    result = namedtuple('Result', ['error', 'payload'])
    payload = {}
    for key in keys:
        try:
            payload[key] = request.json[key]
        except KeyError:
            return False, result(
                error=api_bad_request('missing request parameter: %s' % key),
                payload=None)
    return True, result(error=None, payload=payload)


def _unwrap(keys, dictionary, default=None):
    return [dictionary.get(key, default) for key in keys]


def _create_availability_response(person):
    result = {
         'id': person.id,
         'person': person.full_name,
         'timeslots': [
            {'day': ts.day,
             'hour': int(ts.hour),
             'minute': int(ts.minute)}
            for ts in person.availability]}
    return success(result)
