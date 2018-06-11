import pytest

from app import db
from app.models import Candidate


def test_getting_candidate(client, mockery):
    data = {'first_name': mockery.first_name,
            'last_name': mockery.last_name}

    result = client.json('main.candidate_endpoint', data=data)

    assert result['success']
    assert 'interview' not in result


def test_creating_a_new_candidate(client, drop_candidates):
    data = {'first_name': 'Bob', 'last_name': 'Smith', 'email': 'bob_smith@mail.com'}

    result = client.json('main.candidate_endpoint', data=data, method='POST')

    assert result['success']
    assert 'id' in result
    assert isinstance(result['id'], int)


def test_deleting_candidate(client, mockery):
    data = {'first_name': mockery.first_name,
            'last_name': mockery.last_name}

    result = client.json('main.candidate_endpoint', data=data, method='DELETE')

    assert result['success']
    assert result.get('id') == mockery.id
    assert not Candidate.exists(**data)


# -------------
# Test fixtures
# -------------


@pytest.fixture()
def mockery():
    employee = Candidate(first_name='John',
                         last_name='Doe',
                         email='john_doe@mail.com',
                         skype='john_doe')
    db.session.add(employee)
    db.session.commit()
    yield employee
    db.session.delete(employee)
    db.session.commit()


@pytest.fixture()
def drop_candidates():
    yield None
    for employee in Candidate.query.all():
        db.session.delete(employee)
    db.session.commit()
