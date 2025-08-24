import pytest
from api.models import Comment


@pytest.mark.django_db
def test_comment_creation(student_user, submission):
    comment = Comment.objects.create(
        submission=submission,
        user=student_user,
        content="This is a test comment"
    )

    assert comment.id is not None
    assert comment.submission == submission
    assert comment.user == student_user
    assert comment.content == "This is a test comment"

    expected_str = f'Comment by {student_user.email} on submission {submission.id}'
    assert str(comment) == expected_str


@pytest.mark.django_db
def test_comment_submission_relation(student_user, submission):
    comment1 = Comment.objects.create(submission=submission, user=student_user, content="First comment")
    comment2 = Comment.objects.create(submission=submission, user=student_user, content="Second comment")

    comments = submission.comments.all()
    assert comment1 in comments
    assert comment2 in comments
    assert comments.count() == 2
