import pytest
from api.models import Enrollment
from api.serializers.enrollment import EnrollmentSerializer


@pytest.mark.django_db
def test_enrollment_serializer_creation(student_user, course):
    enrollment = Enrollment.objects.create(user=student_user, course=course)

    serializer = EnrollmentSerializer(enrollment)
    data = serializer.data

    assert data['id'] == enrollment.id
    assert data['user']['id'] == student_user.id
    assert data['user']['email'] == student_user.email
    assert data['course']['id'] == course.id
    assert data['course']['title'] == course.title


@pytest.mark.django_db
def test_enrollment_serializer_duplicate_validation(student_user, course):
    Enrollment.objects.create(user=student_user, course=course)

    serializer = EnrollmentSerializer(data={
        'user': student_user.id,
        'course': course.id
    })

    with pytest.raises(Exception) as exc_info:
        serializer.validate({'user': student_user, 'course': course})

    assert 'already enrolled' in str(exc_info.value)
