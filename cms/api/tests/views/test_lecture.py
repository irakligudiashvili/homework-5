import pytest
from rest_framework.test import APIClient
from api.models import Enrollment, Lecture


@pytest.mark.django_db
def test_lecture_create_success(teacher_user, course, uploaded_file):
    Enrollment.objects.create(user=teacher_user, course=course)

    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {
        "course": course.id,
        "topic": "Test Lecture",
        "file": uploaded_file(name="lecture.pdf")
    }
    response = client.post("/api/v1/lectures/create/", data,
                           format="multipart")

    assert response.status_code == 201
    assert response.data["topic"] == "Test Lecture"
    assert response.data["course"] == course.id


@pytest.mark.django_db
def test_lecture_create_missing_fields(teacher_user):
    client = APIClient()
    client.force_authenticate(user=teacher_user)
    data = {}
    response = client.post("/api/v1/lectures/create/", data,
                           format="multipart")
    assert response.status_code == 400
    assert "course, topic and file are required" in response.data["detail"]


@pytest.mark.django_db
def test_lecture_create_forbidden(student_user, course, uploaded_file):
    client = APIClient()
    client.force_authenticate(user=student_user)

    data = {
        "course": course.id,
        "topic": "Lecture",
        "file": uploaded_file(name="lecture.pdf")
    }
    response = client.post("/api/v1/lectures/create/", data, format="multipart")

    assert response.status_code == 403
    assert "permission" in str(response.data["detail"]).lower()


@pytest.mark.django_db
def test_lecture_list_access(teacher_user, student_user, course, lecture):
    from api.models import Enrollment
    client = APIClient()

    Enrollment.objects.create(user=student_user, course=course)

    client.force_authenticate(user=teacher_user)
    response = client.get(f"/api/v1/lectures/course/{course.id}/")
    assert response.status_code == 200
    assert len(response.data) >= 1

    client.force_authenticate(user=student_user)
    response = client.get(f"/api/v1/lectures/course/{course.id}/")
    assert response.status_code == 200

    new_user = teacher_user
    client.force_authenticate(user=new_user)
    response = client.get(f"/api/v1/lectures/course/{course.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_lecture_update_by_owner(teacher_user, course, lecture):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    data = {"topic": "Updated Topic"}
    response = client.patch(f"/api/v1/lectures/{lecture.id}/update/", data)
    assert response.status_code == 200
    assert response.data["topic"] == "Updated Topic"


@pytest.mark.django_db
def test_lecture_update_forbidden(student_user, lecture):
    client = APIClient()
    client.force_authenticate(user=student_user)

    data = {"topic": "Hacked Topic"}
    response = client.patch(f"/api/v1/lectures/{lecture.id}/update/", data)
    assert response.status_code == 403
    assert "permission" in response.data["detail"].lower()


@pytest.mark.django_db
def test_lecture_delete_by_owner(teacher_user, lecture):
    client = APIClient()
    client.force_authenticate(user=teacher_user)

    response = client.delete(f"/api/v1/lectures/{lecture.id}/delete/")
    assert response.status_code == 204
    assert not Lecture.objects.filter(id=lecture.id).exists()


@pytest.mark.django_db
def test_lecture_delete_forbidden(student_user, lecture):
    client = APIClient()
    client.force_authenticate(user=student_user)

    response = client.delete(f"/api/v1/lectures/{lecture.id}/delete/")
    assert response.status_code == 403
