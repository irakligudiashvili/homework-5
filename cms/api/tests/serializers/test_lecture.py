import pytest
from api.models import Lecture, Assignment
from api.serializers.lecture import LectureSerializer


@pytest.mark.django_db
def test_lecture_serializer_basic(course):
    lecture = Lecture.objects.create(
        course=course,
        topic="Test Lecture",
        file="lectures/test_file.pdf"
    )

    serializer = LectureSerializer(lecture)
    data = serializer.data

    assert data['id'] == lecture.id
    assert data['course'] == lecture.course.id
    assert data['topic'] == "Test Lecture"
    assert data['file'].endswith('lectures/test_file.pdf')
    assert data['assignments'] == []


@pytest.mark.django_db
def test_lecture_serializer_with_assignments(course):
    lecture = Lecture.objects.create(
        course=course,
        topic="Lecture with Assignment",
        file="lectures/file.pdf"
    )

    Assignment.objects.create(
        lecture=lecture,
        title="Assignment 1",
        description="Desc 1"
    )
    Assignment.objects.create(
        lecture=lecture,
        title="Assignment 2",
        description="Desc 2"
    )

    serializer = LectureSerializer(lecture)
    data = serializer.data

    assignment_ids = [a for a in data['assignments']]
    assert len(assignment_ids) == 2
