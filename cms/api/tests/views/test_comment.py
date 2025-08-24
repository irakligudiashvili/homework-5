import pytest
from rest_framework.test import APIClient
from api.models import Course, Lecture, Assignment, Submission, Comment, Enrollment


@pytest.mark.django_db
def test_comment_create(student_user, teacher_user):
    client = APIClient()

    course = Course.objects.create(title="Course", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture", file="lectures/file.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file.pdf")

    client.force_authenticate(user=student_user)
    response = client.post("/api/v1/comments/create/", data={
        "submission": submission.id,
        "content": "This is a comment"
    })

    assert response.status_code == 201
    data = response.json()
    assert data['content'] == "This is a comment"
    assert data['user'] == str(student_user)
    assert data['submission'] == submission.id


@pytest.mark.django_db
def test_comment_list(student_user, teacher_user):
    client = APIClient()

    course = Course.objects.create(title="Course", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture", file="lectures/file.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file.pdf")

    comment = Comment.objects.create(submission=submission, user=student_user, content="Hello comment")

    client.force_authenticate(user=student_user)

    response = client.get(f"/api/v1/submissions/{submission.id}/comments/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]['content'] == "Hello comment"



@pytest.mark.django_db
def test_comment_update(student_user, teacher_user):
    client = APIClient()

    course = Course.objects.create(title="Course", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture", file="lectures/file.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file.pdf")
    comment = Comment.objects.create(submission=submission, user=student_user, content="Original")

    client.force_authenticate(user=student_user)
    response = client.patch(f"/api/v1/comments/{comment.id}/update/", data={"content": "Updated"})
    assert response.status_code == 200
    comment.refresh_from_db()
    assert comment.content == "Updated"


@pytest.mark.django_db
def test_comment_delete(student_user, teacher_user):
    client = APIClient()

    course = Course.objects.create(title="Course", description="Desc", owner=teacher_user)
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture = Lecture.objects.create(course=course, topic="Lecture", file="lectures/file.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment", description="Desc")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file="sub/file.pdf")
    comment = Comment.objects.create(submission=submission, user=student_user, content="To be deleted")

    client.force_authenticate(user=student_user)
    response = client.delete(f"/api/v1/comments/{comment.id}/delete/")
    assert response.status_code == 204
    assert not Comment.objects.filter(id=comment.id).exists()
