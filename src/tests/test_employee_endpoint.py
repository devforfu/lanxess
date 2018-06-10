import pytest

from app import db
from app.models import Employee, Candidate, Interview


def test_getting_employee(client, mockery):
    data = {'first_name': mockery.first_name,
            'last_name': mockery.last_name}

    result = client.json('main.employee_endpoint', data=data)

    assert result['success']
    assert 'interviews' in result
    assert len(result['interviews']) == 0


def test_creating_a_new_employee(client, drop_employees):
    data = {'first_name': 'Bob', 'last_name': 'Smith'}

    result = client.json('main.employee_endpoint', data=data, method='POST')

    assert result['success']
    assert 'id' in result
    assert isinstance(result['id'], int)


def test_deleting_employee(client, mockery):
    data = {'first_name': mockery.first_name,
            'last_name': mockery.last_name}

    result = client.json('main.employee_endpoint', data=data, method='DELETE')

    assert result['success']
    assert result.get('id') == mockery.id
    assert not Employee.exists(**data)


# -------------
# Test fixtures
# -------------


@pytest.fixture()
def mockery():
    employee = Employee(first_name='John', last_name='Doe')
    db.session.add(employee)
    db.session.commit()
    yield employee
    db.session.delete(employee)
    db.session.commit()


@pytest.fixture()
def drop_employees():
    yield None
    for employee in Employee.query.all():
        db.session.delete(employee)
    db.session.commit()
