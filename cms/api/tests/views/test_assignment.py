import pytest
from rest_framework.test import APIClient
from api.models import Lecture, Assignment, Enrollment, Course


@pytest.mark.django_db
def test_assignment_create_success(teacher_user, course, uploaded_file):
    Enrollment.objects.create(user=teacher_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture 1", file=uploaded_file(name="lecture.pdf"))
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {
        "lecture": lecture.id,
        "title": "Test Assignment",
        "description": "Assignment description"
    }

    response = client.post("/api/v1/assignments/create/", data)
    assert response.status_code == 201
    assert response.data["title"] == "Test Assignment"


@pytest.mark.django_db
def test_assignment_create_missing_fields(teacher_user, course):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    response = client.post("/api/v1/assignments/create/", data={})
    assert response.status_code == 400
    assert "Lecture and title are required" in str(response.data["detail"])


@pytest.mark.django_db
def test_assignment_create_forbidden(student_user, course, uploaded_file):
    lecture = Lecture.objects.create(course=course, topic="Lecture 1", file=uploaded_file(name="lecture.pdf"))
    client = APIClient()
    client.force_authenticate(user=student_user)

    data = {
        "lecture": lecture.id,
        "title": "Forbidden Assignment"
    }

    response = client.post("/api/v1/assignments/create/", data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_assignment_list_access(teacher_user, student_user, django_user_model):
    client = APIClient()

    course = Course.objects.create(title="Test Course", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Test Lecture", file="lectures/file.pdf")

    assignment1 = Assignment.objects.create(lecture=lecture, title="Assignment 1", description="Desc 1")
    assignment2 = Assignment.objects.create(lecture=lecture, title="Assignment 2", description="Desc 2")

    url = f"/api/v1/assignments/lecture/{lecture.id}/"

    client.force_authenticate(user=teacher_user)
    response = client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    client.force_authenticate(user=None)

    client.force_authenticate(user=student_user)
    response = client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    client.force_authenticate(user=None)

    outsider = django_user_model.objects.create_user(
        email="outsider@test.com",
        password="pass123",
        role="student"
    )
    client.force_authenticate(user=outsider)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_assignment_detail_update_delete(teacher_user, course, uploaded_file):
    Enrollment.objects.create(user=teacher_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture 1", file=uploaded_file(name="lecture.pdf"))
    assignment = Assignment.objects.create(lecture=lecture, title="Original", description="Original desc")

    client = APIClient()
    client.force_authenticate(user=teacher_user)

    response = client.get(f"/api/v1/assignments/{assignment.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Original"

    data = {"title": "Updated"}
    response = client.patch(f"/api/v1/assignments/{assignment.id}/update/", data)
    assert response.status_code == 200
    assert response.data["title"] == "Updated"

    response = client.delete(f"/api/v1/assignments/{assignment.id}/delete/")
    assert response.status_code == 204
    assert Assignment.objects.filter(id=assignment.id).count() == 0
