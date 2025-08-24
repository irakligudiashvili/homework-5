import pytest
from rest_framework.test import APIClient
from api.models import Course, Enrollment


@pytest.mark.django_db
def test_course_create_view(teacher_user):
    api_client = APIClient()
    api_client.force_authenticate(user=teacher_user)

    data = {"title": "New Course", "description": "Course desc"}
    response = api_client.post("/api/v1/courses/create/", data)

    assert response.status_code == 201
    course = Course.objects.get(title="New Course")
    assert course.owner == teacher_user
    enrollment = Enrollment.objects.get(user=teacher_user, course=course)
    assert enrollment is not None


@pytest.mark.django_db
def test_course_create_forbidden_for_student(student_user):
    api_client = APIClient()
    api_client.force_authenticate(user=student_user)

    data = {"title": "Student Course", "description": "Desc"}
    response = api_client.post("/api/v1/courses/create/", data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_course_update_view(teacher_user, course):
    api_client = APIClient()
    api_client.force_authenticate(user=teacher_user)

    data = {"description": "Updated description"}
    response = api_client.patch(f"/api/v1/courses/{course.id}/update/", data)

    assert response.status_code == 200
    course.refresh_from_db()
    assert course.description == "Updated description"


@pytest.mark.django_db
def test_course_delete_view(teacher_user, course):
    api_client = APIClient()
    api_client.force_authenticate(user=teacher_user)

    response = api_client.delete(f"/api/v1/courses/{course.id}/delete/")

    assert response.status_code == 204
    assert Course.objects.filter(id=course.id).count() == 0


@pytest.mark.django_db
def test_course_list_view(teacher_user, student_user, course):
    api_client = APIClient()
    api_client.force_authenticate(user=teacher_user)

    Enrollment.objects.get_or_create(user=teacher_user, course=course)

    response = api_client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert any(c['id'] == course.id for c in data)

    api_client.force_authenticate(user=student_user)
    Enrollment.objects.get_or_create(user=student_user, course=course)
    response = api_client.get("/api/v1/courses/")
    data = response.json()
    assert any(c['id'] == course.id for c in data)
