import pytest
from api.models import Lecture


@pytest.mark.django_db
def test_lecture_creation(course):
    lecture = Lecture.objects.create(
        course=course,
        topic='Test Lecture',
        file='lectures/test_file.pdf'
    )
    assert lecture.id is not None
    assert lecture.topic == 'Test Lecture'
    assert lecture.course == course
    assert str(lecture) == 'Test Lecture'


@pytest.mark.django_db
def test_lecture_course_relation(course):
    lecture1 = Lecture.objects.create(course=course, topic='Lecture 1', file='lectures/file1.pdf')
    lecture2 = Lecture.objects.create(course=course, topic='Lecture 2', file='lectures/file2.pdf')

    lectures = course.lectures.all()
    assert lecture1 in lectures
    assert lecture2 in lectures
    assert lectures.count() == 2
