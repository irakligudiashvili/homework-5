import pytest
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Submission, Assignment, Lecture
from api.serializers.submission import SubmissionSerializer


@pytest.mark.django_db
def test_submission_serializer_basic(student_user, course):
    lecture = Lecture.objects.create(
        course=course,
        topic="Lecture 1",
        file="lectures/file1.pdf"
    )
    assignment = Assignment.objects.create(
        lecture=lecture,
        title="Assignment 1",
        description="Test assignment"
    )

    file = SimpleUploadedFile("test_submission.pdf", b"file_content", content_type="application/pdf")
    submission = Submission.objects.create(
        user=student_user,
        assignment=assignment,
        file=file
    )

    serializer = SubmissionSerializer(submission)
    data = serializer.data

    assert data['id'] == submission.id
    assert data['user'] == student_user.id
    assert data['assignment'] == assignment.id

    actual_file_name = os.path.basename(data['file'])
    assert actual_file_name.startswith('test_submission')
    assert actual_file_name.endswith('.pdf')


@pytest.mark.django_db
def test_submission_serializer_create(student_user, course):
    lecture = Lecture.objects.create(course=course, topic="Lecture 2", file="lectures/file2.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 2", description="Desc")

    file = SimpleUploadedFile("upload.pdf", b"data", content_type="application/pdf")
    request_context = {'request': type('Request', (), {'user': student_user})()}

    serializer = SubmissionSerializer(
        data={'assignment': assignment.id, 'file': file},
        context=request_context
    )
    assert serializer.is_valid()
    submission = serializer.save()

    assert submission.user == student_user
    assert submission.assignment == assignment

    actual_file_name = os.path.basename(submission.file.name)
    assert actual_file_name.startswith('upload')
    assert actual_file_name.endswith('.pdf')
