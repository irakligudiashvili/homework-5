import pytest
from api.models import Submission
import os


@pytest.mark.django_db
def test_submission_creation(student_user, assignment, uploaded_file):
    file = uploaded_file(name='test_submission.pdf')

    submission = Submission.objects.create(
        user=student_user,
        assignment=assignment,
        file=file
    )

    assert submission.id is not None
    assert submission.user == student_user
    assert submission.assignment == assignment

    actual_file_name = os.path.basename(submission.file.name)
    assert actual_file_name.startswith('test_submission')
    assert actual_file_name.endswith('.pdf')

    expected_str = f"Submission by {submission.user.email} for {submission.assignment.title}"
    assert str(submission) == expected_str


@pytest.mark.django_db
def test_submission_assignment_relation(student_user, assignment, uploaded_file):
    file1 = uploaded_file(name='file1.pdf')
    file2 = uploaded_file(name='file2.pdf')

    submission1 = Submission.objects.create(user=student_user, assignment=assignment, file=file1)
    submission2 = Submission.objects.create(user=student_user, assignment=assignment, file=file2)

    submissions = assignment.submissions.all()
    assert submission1 in submissions
    assert submission2 in submissions
    assert submissions.count() == 2
