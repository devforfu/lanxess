import pytest

from app import db
from app.models import Employee


def test_allocating_free_timeslot_for_employee(client, mock_employee):
    data = {'employee_id': mock_employee.id, 'day': 'Tuesday', 'time': '12:33'}

    result = client.json('main.allocate_employee_time', method='POST', data=data)

    assert result['success']
    assert len(result['timeslots']) == 1
    assert result['timeslots'][0]['day'] == data['day']
    assert result['timeslots'][0]['hour'] == 12
    assert result['timeslots'][0]['minute'] == 30


# -------------
# Test fixtures
# -------------


@pytest.fixture()
def mock_employee():
    employee = Employee(first_name='John', last_name='Doe')
    db.session.add(employee)
    db.session.commit()
    yield employee
    db.session.delete(employee)
    db.session.commit()
