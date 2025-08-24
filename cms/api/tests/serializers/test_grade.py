import pytest
from api.models import Grade, Submission, Assignment, Lecture
from api.serializers.grade import GradeSerializer
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_grade_serializer_basic(student_user, teacher_user, course):
    lecture = Lecture.objects.create(course=course, topic="Lecture 1", file="lectures/file1.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 1", description="Desc")

    file = SimpleUploadedFile("file.pdf", b"data", content_type="application/pdf")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file=file)

    grade = Grade.objects.create(submission=submission, teacher=teacher_user, score=95)

    serializer = GradeSerializer(grade)
    data = serializer.data

    assert data['id'] == grade.id
    assert data['submission'] == submission.id
    assert data['teacher'] == teacher_user.id
    assert data['score'] == 95


@pytest.mark.django_db
def test_grade_serializer_score_validation(student_user, teacher_user, course):
    lecture = Lecture.objects.create(course=course, topic="Lecture 2", file="lectures/file2.pdf")
    assignment = Assignment.objects.create(lecture=lecture, title="Assignment 2", description="Desc")

    file = SimpleUploadedFile("file2.pdf", b"data", content_type="application/pdf")
    submission = Submission.objects.create(user=student_user, assignment=assignment, file=file)

    serializer = GradeSerializer(
        data={'submission': submission.id, 'score': 150})
    assert not serializer.is_valid()
    assert 'score' in serializer.errors
    assert serializer.errors['score'][0].code == 'max_value'

    serializer = GradeSerializer(data={'submission': submission.id, 'score': 85})
    assert serializer.is_valid()
