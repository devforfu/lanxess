import pytest

from app import db
from app.models import Employee, Candidate, Timeslot


def test_get_timeslots_for_candidate_and_interviewers(client, mockery):
    employee1, employee2, candidate = mockery
    data = {'candidate': candidate.id, 'employees': [employee1.id, employee2.id]}

    result = client.json('main.list_interviews', data=data)

    assert result['success']
    assert 'schedule' in result
    assert len(result['schedule']) == 3


# -------------
# Test fixtures
# -------------


@pytest.fixture()
def mockery():
    timeslots = [
        Timeslot(day='Monday', hour='10', minute='0'),    # 0
        Timeslot(day='Monday', hour='10', minute='15'),   # 1
        Timeslot(day='Monday', hour='10', minute='30'),   # 2
        Timeslot(day='Monday', hour='10', minute='45'),   # 3
        Timeslot(day='Monday', hour='11', minute='0'),    # 4
        Timeslot(day='Monday', hour='11', minute='15'),   # 5
        Timeslot(day='Monday', hour='11', minute='30'),   # 6
        Timeslot(day='Tuesday', hour='12', minute='0'),   # 7
        Timeslot(day='Tuesday', hour='12', minute='15'),  # 8
        Timeslot(day='Tuesday', hour='12', minute='30'),  # 9
        Timeslot(day='Tuesday', hour='12', minute='45'),  # 10
        Timeslot(day='Friday', hour='14', minute='0'),    # 11
        Timeslot(day='Friday', hour='14', minute='15')    # 12
    ]

    employee1 = Employee(
        first_name='John',
        last_name='Doe',
        availability=timeslots[:7],
    )

    employee2 = Employee(
        first_name='Bob',
        last_name='Smith',
        availability=timeslots[5:]
    )

    candidate = Candidate(
        first_name='Alice',
        last_name='Appleseed',
        email='alice_appleseed@mail.com',
        availability=[timeslots[7], timeslots[8], timeslots[11]]
    )

    for obj in (employee1, employee2, candidate):
        db.session.add(obj)
    db.session.commit()

    yield employee1, employee2, candidate

    for obj in (employee1, employee2, candidate):
        db.session.delete(obj)
    db.session.commit()
