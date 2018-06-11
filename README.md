# Backend Developer Assessment

We are hiring a lot of excellent people at Lanxess. And it is often a challenge to set up an interview, since our managers might have quite busy schedules. So we’d like to ask you to build a prototype of an app that makes this process a little bit easier.

Build a bundle of REST interfaces (only apis are asked, no visual interfaces are needed) that allow to do the following:

  1. Manage a list of employees who are making the interviews
  1. Manage a list of potential candidates
  1. Submit availability for the employee/candidate for the next week (that means, the list of
    days of the week / hours available for the interview). For simplicity, we assume that we always deal with one specific week only (in other words, on Friday evening the assistant is making plans for the coming week). But you’re welcome to extend the task!
  1. Receive a list of time slots to make an interview (providing a candidate and list of interviewers required). If there is no time slot available during next week, the service should return an appropriate error.
  1. You are welcome to use any additional frameworks you wish.

  And please do not hesitate to ask if something in the task looks unclear to you. Have fun!


# Solution

I've decided to approach this problem with setting a set of constraints
to reduce the scope of the task. First of all, I've assumed that
interviews usually scheduled on more or less "round" times, like 14:45
or 17:00, and not like 13:18. Therefore, my approach was to split
time into the discrete time slots with 15 minutes duration, like:

```
Monday, 10:00
Monday, 10:15
Monday, 10:30
...
Friday, 18:00
```

Both `Employee` and `Candidate` have their lists of available timeslots.
In this case, the task to find time slots that are available for
both candidate and employee becomes quite simple - one only need to
search for equal timeslots.

Note that there is a specific behaviour in `/api/v1/allocate_employee_time`
(same for candidates, but I didn't finish this part) when a new timeslot is created.
If the same timeslot (with same day, hour and minute) exists in database, it
is returned instead of being created again. That's why we can use `in`
operator in `list_interviews` endpoint to find common timeslots.

List of technologies:
* miniconda
* Python v3.6
* Flask (+ plugins)
* SQLAlchemy
* pytest
* PostgreSQL
* Vagrant

Unfortunately, I wasn't able to complete my idea in time and the final
API is not really usable yet. There is possibility to create some of
models and to list interviews, but there is no way, for example,
to update candidates. These endpoints are implemented as stubs
returning error.