import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from api.models import User, Course, Lecture, Assignment, Submission, \
    Grade, Comment


@pytest.fixture
def api_client():
    return APIClient()


# Users
@pytest.fixture
def teacher_user(db):
    return User.objects.create_user(
        first_name='Teacher',
        last_name='One',
        email='teacher@gmail.com',
        password='123',
        role='teacher'
    )


@pytest.fixture
def student_user(db):
    return User.objects.create_user(
        first_name='Student',
        last_name='One',
        email='student@gmail.com',
        password='123',
        role='student'
    )


# Course
@pytest.fixture
def course(db, teacher_user):
    return Course.objects.create(
        title='Test Course',
        description='A test course',
        owner=teacher_user
    )


# Lectures
@pytest.fixture
def lecture(db, course):
    return Lecture.objects.create(
        course=course,
        topic='Test Lecture',
        file='lectures/test_file.pdf'
    )


# Assignments
@pytest.fixture
def assignment(db, lecture):
    return Assignment.objects.create(
        lecture=lecture,
        title='Test Assignment',
        description='Assignment description'
    )


# Submissions
@pytest.fixture
def submission(db, student_user, assignment):
    return Submission.objects.create(
        user=student_user,
        assignment=assignment,
        file='submission/test_file.pdf'
    )


# SimpleUploadedFile
@pytest.fixture
def uploaded_file():
    def _uploaded_file(
        name='test.pdf',
        content=b'Test file content',
        content_type='application/pdf'
    ):
        return SimpleUploadedFile(
            name=name,
            content=content,
            content_type=content_type
        )

    return _uploaded_file


# Grades
@pytest.fixture
def grade(db, submission, teacher_user):
    return Grade.objects.create(
        submission=submission,
        teacher=teacher_user,
        score=100
    )


# Comments
@pytest.fixture
def comment(db, submission, student_user):
    return Comment.objects.create(
        submission=submission,
        user=student_user,
        content="Test comment"
    )
