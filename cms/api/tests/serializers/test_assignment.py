import pytest
from api.models import Assignment, Lecture
from api.serializers.assignment import AssignmentSerializer


@pytest.mark.django_db
def test_assignment_serializer_basic(course):
    lecture = Lecture.objects.create(
        course=course,
        topic="Test Lecture",
        file="lectures/test_file.pdf"
    )

    assignment = Assignment.objects.create(
        lecture=lecture,
        title="Test Assignment",
        description="Assignment description"
    )

    serializer = AssignmentSerializer(assignment)
    data = serializer.data

    assert data['id'] == assignment.id
    assert data['title'] == "Test Assignment"
    assert data['description'] == "Assignment description"


@pytest.mark.django_db
def test_assignment_serializer_update(course):
    lecture = Lecture.objects.create(
        course=course,
        topic="Lecture for Update",
        file="lectures/file.pdf"
    )

    assignment = Assignment.objects.create(
        lecture=lecture,
        title="Old Title",
        description="Old description"
    )

    serializer = AssignmentSerializer(
        assignment,
        data={'title': 'New Title', 'description': 'New description'},
        partial=True
    )
    assert serializer.is_valid()
    updated = serializer.save()

    assert updated.title == "New Title"
    assert updated.description == "New description"
