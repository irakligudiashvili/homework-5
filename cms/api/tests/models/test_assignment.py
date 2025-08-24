import pytest
from api.models import Assignment


@pytest.mark.django_db
def test_assignment_creation(lecture):
    assignment = Assignment.objects.create(
        lecture=lecture,
        title='Test Assignment',
        description='This is a test assignment'
    )

    assert assignment.id is not None
    assert assignment.title == 'Test Assignment'
    assert assignment.description == 'This is a test assignment'
    assert assignment.lecture == lecture
    assert str(assignment) == f'Test Assignment (Lecture: {lecture.topic})'


@pytest.mark.django_db
def test_assignment_lecture_relation(lecture):
    assignment1 = Assignment.objects.create(
        lecture=lecture,
        title='Assignment 1',
        description='First assignment'
    )
    assignment2 = Assignment.objects.create(
        lecture=lecture,
        title='Assignment 2',
        description='Second assignment'
    )

    assignments = lecture.assignments.all()
    assert assignment1 in assignments
    assert assignment2 in assignments
    assert assignments.count() == 2
