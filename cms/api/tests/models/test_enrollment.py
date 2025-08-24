import pytest
from django.db import IntegrityError
from api.models import Enrollment


@pytest.mark.django_db
def test_enrollment_creation(student_user, course):
    enrollment = Enrollment.objects.create(user=student_user, course=course)

    assert enrollment.id is not None
    assert enrollment.user == student_user
    assert enrollment.course == course
    assert str(enrollment) == f'{student_user} enrolled in {course}'
    assert enrollment in student_user.enrollments.all()
    assert enrollment in course.enrollments.all()
    assert student_user in course.students.all()


@pytest.mark.django_db
def test_unique_enrollment_constraint(student_user, course):
    Enrollment.objects.create(user=student_user, course=course)

    with pytest.raises(IntegrityError):
        Enrollment.objects.create(user=student_user, course=course)


@pytest.mark.django_db
def test_multiple_enrollments(course, teacher_user, student_user):
    enrollment1 = Enrollment.objects.create(user=teacher_user, course=course)
    enrollment2 = Enrollment.objects.create(user=student_user, course=course)

    students = course.students.all()
    assert teacher_user in students
    assert student_user in students
    assert students.count() == 2
