import pytest
from api.models import Course


@pytest.mark.django_db
def test_course_creation(teacher_user):
    course = Course.objects.create(
        title='Test Course',
        description='A test course',
        owner=teacher_user
    )
    assert course.id is not None
    assert course.title == 'Test Course'
    assert course.owner == teacher_user
    assert str(course) == 'Test Course'
