import pytest
import os
from rest_framework.test import APIClient
from api.models import Course, Lecture, Assignment, Submission, Enrollment

@pytest.mark.django_db
def test_submission_create(student_user, teacher_user, uploaded_file):
    client = APIClient()

    course = Course.objects.create(title="Course", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=student_user, course=course)
    lecture = Lecture.objects.create(course=course, topic="Lecture 1", file="lectures/file1.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 1", description="Desc")

    client.force_authenticate(user=student_user)
    file_obj = uploaded_file(name="submission.pdf")
    response = client.post(
        "/api/v1/submissions/create/",
        {"assignment": assignment.id, "file": file_obj},
        format='multipart'
    )

    assert response.status_code == 201
    data = response.json()
    submission = Submission.objects.get(id=data['id'])

    assert submission.user == student_user
    assert submission.assignment == assignment

    file_name = os.path.basename(submission.file.name)
    assert file_name.startswith("submission")
    assert file_name.endswith(".pdf")


@pytest.mark.django_db
def test_submission_create_forbidden_not_enrolled(student_user, teacher_user, uploaded_file):
    client = APIClient()

    course = Course.objects.create(title="Course 2", description="Desc", owner=teacher_user)
    lecture = Lecture.objects.create(course=course, topic="Lecture 2", file="lectures/file2.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 2", description="Desc")

    client.force_authenticate(user=student_user)
    file_obj = uploaded_file(name="submission2.pdf")
    response = client.post(
        "/api/v1/submissions/create/",
        {"assignment": assignment.id, "file": file_obj},
        format='multipart'
    )

    assert response.status_code == 403
    assert "not enrolled" in response.json()['detail']


@pytest.mark.django_db
def test_submission_list_student(student_user, teacher_user):
    client = APIClient()
    course = Course.objects.create(title="Course 3", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=student_user, course=course)
    lecture = Lecture.objects.create(course=course, topic="Lecture 3", file="lectures/file3.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 3", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file3.pdf")

    client.force_authenticate(user=student_user)
    response = client.get("/api/v1/submissions/")
    assert response.status_code == 200
    data = response.json()
    assert any(s['id'] == submission.id for s in data)


@pytest.mark.django_db
def test_submission_list_teacher(student_user, teacher_user):
    client = APIClient()
    course = Course.objects.create(title="Course 4", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)
    lecture = Lecture.objects.create(course=course, topic="Lecture 4", file="lectures/file4.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 4", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file4.pdf")

    client.force_authenticate(user=teacher_user)
    response = client.get("/api/v1/submissions/")
    assert response.status_code == 200
    data = response.json()
    assert any(s['id'] == submission.id for s in data)


@pytest.mark.django_db
def test_submission_retrieve(student_user, teacher_user):
    client = APIClient()
    course = Course.objects.create(title="Course 5", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=student_user, course=course)
    Enrollment.objects.create(user=teacher_user, course=course)
    lecture = Lecture.objects.create(course=course, topic="Lecture 5", file="lectures/file5.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 5", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file5.pdf")

    client.force_authenticate(user=student_user)
    response = client.get(f"/api/v1/submissions/{submission.id}/")
    assert response.status_code == 200
    assert response.json()['id'] == submission.id

    client.force_authenticate(user=teacher_user)
    response = client.get(f"/api/v1/submissions/{submission.id}/")
    assert response.status_code == 200
    assert response.json()['id'] == submission.id
