import pytest
from rest_framework.test import APIClient
from api.models import Enrollment


@pytest.mark.django_db
def test_enroll_in_course_success(teacher_user, student_user, course):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {"course_id": course.id, "user_id": student_user.id}
    response = client.post("/api/v1/courses/enroll/", data)

    assert response.status_code == 201
    enrollment = Enrollment.objects.get(user=student_user, course=course)
    assert enrollment is not None
    assert response.data['user']['id'] == student_user.id
    assert response.data['course']['id'] == course.id


@pytest.mark.django_db
def test_enroll_in_course_missing_fields(teacher_user):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    response = client.post("/api/v1/courses/enroll/",{})
    assert response.status_code == 400
    assert 'course_id and user_id are required' in response.data['detail']


@pytest.mark.django_db
def test_enroll_in_course_nonexistent_course(teacher_user, student_user):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {"course_id": 9999, "user_id": student_user.id}
    response = client.post("/api/v1/courses/enroll/", data)
    assert response.status_code == 404
    assert 'Course not found' in response.data['detail']


@pytest.mark.django_db
def test_enroll_in_course_nonexistent_user(teacher_user, course):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {"course_id": course.id, "user_id": 9999}
    response = client.post("/api/v1/courses/enroll/", data)
    assert response.status_code == 404
    assert 'User not found' in response.data['detail']


@pytest.mark.django_db
def test_enroll_in_course_already_enrolled(teacher_user, student_user, course):
    Enrollment.objects.create(user=student_user, course=course)
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {"course_id": course.id, "user_id": student_user.id}
    response = client.post("/api/v1/courses/enroll/", data)
    assert response.status_code == 400
    assert 'User is already enrolled' in response.data['detail']


@pytest.mark.django_db
def test_unenroll_success(teacher_user, student_user, course):
    Enrollment.objects.create(user=student_user, course=course)
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {"course_id": course.id, "user_id": student_user.id}
    response = client.delete("/api/v1/courses/unenroll/", data, format='json')

    assert response.status_code == 200
    assert 'User unenrolled' in response.data['detail']
    assert Enrollment.objects.filter(user=student_user,
                                     course=course).count() == 0


@pytest.mark.django_db
def test_unenroll_course_owner_not_allowed(teacher_user, course):
    Enrollment.objects.create(user=teacher_user, course=course)

    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {"course_id": course.id, "user_id": teacher_user.id}
    response = client.delete("/api/v1/courses/unenroll/", data, format='json')

    assert response.status_code == 400
    assert 'Course owner cannot be unenrolled' in response.data['detail']



@pytest.mark.django_db
def test_unenroll_user_not_enrolled(teacher_user, student_user, course):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {"course_id": course.id, "user_id": student_user.id}
    response = client.delete("/api/v1/courses/unenroll/", data, format='json')

    assert response.status_code == 404
    assert 'User is not enrolled in this course' in response.data['detail']


@pytest.mark.django_db
def test_unenroll_missing_fields(teacher_user):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    response = client.delete("/api/v1/courses/unenroll/", {}, format='json')
    assert response.status_code == 400
    assert 'course_id and user_id are required' in response.data['detail']
