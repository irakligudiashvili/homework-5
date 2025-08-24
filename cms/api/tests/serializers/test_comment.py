import pytest
from api.serializers.comment import CommentSerializer


@pytest.mark.django_db
def test_comment_serializer_creation(student_user, submission, rf):
    request = rf.post("/fake-url/")
    request.user = student_user

    data = {
        "submission": submission.id,
        "content": "This is a test comment"
    }

    serializer = CommentSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors

    comment = serializer.save()

    assert comment.id is not None
    assert comment.user == student_user
    assert comment.submission == submission
    assert comment.content == "This is a test comment"

    expected_str = f"Comment by {student_user.email} on submission {submission.id}"
    assert str(comment) == expected_str


@pytest.mark.django_db
def test_comment_serializer_read_only_user(student_user, submission, rf):
    request = rf.post("/fake-url/")
    request.user = student_user

    data = {
        "submission": submission.id,
        "content": "Another comment",
        "user": 999
    }

    serializer = CommentSerializer(data=data, context={"request": request})
    assert serializer.is_valid(), serializer.errors

    comment = serializer.save()
    assert comment.user == student_user
