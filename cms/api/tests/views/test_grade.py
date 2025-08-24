import pytest
from rest_framework.test import APIClient
from api.models import Course, Lecture, Assignment, Submission, Grade, Enrollment


@pytest.mark.django_db
def test_grade_create(student_user, teacher_user):
    client = APIClient()

    course = Course.objects.create(title="Course", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture 1", file="lectures/file1.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 1", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file1.pdf")

    client.force_authenticate(user=teacher_user)
    response = client.post("/api/v1/grades/create/", data={"submission": submission.id, "score": 90})
    assert response.status_code == 201


@pytest.mark.django_db
def test_grade_create_forbidden_not_enrolled(student_user, teacher_user):
    client = APIClient()

    course = Course.objects.create(title="Course 2", description="Desc",
                                   owner=teacher_user)
    lecture = Lecture.objects.create(course=course, topic="Lecture 2",
                                     file="lectures/file2.pdf")
    assignment = Assignment.objects.create(lecture=lecture,
                                           title="Assignment 2",
                                           description="Desc")
    submission = Submission.objects.create(user=student_user,
                                           assignment=assignment,
                                           file="sub/file2.pdf")

    client.force_authenticate(user=teacher_user)
    response = client.post("/api/v1/grades/create/",
                           data={"submission": submission.id, "score": 85})

    assert response.status_code == 403
    assert "enrolled" in response.json()['detail']


@pytest.mark.django_db
def test_grade_retrieve(student_user, teacher_user):
    client = APIClient()
    course = Course.objects.create(title="Course 3", description="Desc", owner=teacher_user)

    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture 3", file="lectures/file3.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 3", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file3.pdf")
    grade = Grade.objects.create(submission=submission, teacher=teacher_user, score=95)

    client.force_authenticate(user=student_user)
    response = client.get(f"/api/v1/grades/{grade.id}/")

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == grade.id
    assert data['score'] == grade.score
    assert data['teacher'] == teacher_user.id



@pytest.mark.django_db
def test_grade_update(student_user, teacher_user):
    client = APIClient()
    course = Course.objects.create(title="Course 4", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture 4", file="lectures/file4.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 4", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file4.pdf")
    grade = Grade.objects.create(submission=submission, teacher=teacher_user, score=70)

    client.force_authenticate(user=teacher_user)
    response = client.patch(f"/api/v1/grades/{grade.id}/update/", data={"score": 88})
    assert response.status_code == 200
    grade.refresh_from_db()
    assert grade.score == 88


@pytest.mark.django_db
def test_grade_delete(student_user, teacher_user):
    client = APIClient()
    course = Course.objects.create(title="Course 5", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture 5", file="lectures/file5.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 5", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file5.pdf")
    grade = Grade.objects.create(submission=submission, teacher=teacher_user, score=77)

    client.force_authenticate(user=teacher_user)
    response = client.delete(f"/api/v1/grades/{grade.id}/delete/")
    assert response.status_code == 204
    assert not Grade.objects.filter(id=grade.id).exists()
