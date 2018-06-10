"""
Interviews management API.
"""
from collections import namedtuple

from flask import jsonify, request, current_app
from werkzeug.exceptions import HTTPException

from . import main
from ..models import Employee, Candidate


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
            fullname = '{first_name} {last_name}'.format(**payload)
            return api_bad_request(f'employee not found: {fullname}')

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

    return api_bad_request('not implemented')


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
