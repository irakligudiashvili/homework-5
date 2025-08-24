import pytest
from api.models import Grade


@pytest.mark.django_db
def test_grade_creation(submission, teacher_user):
    grade = Grade.objects.create(
        submission=submission,
        teacher=teacher_user,
        score=85
    )

    assert grade.id is not None
    assert grade.submission == submission
    assert grade.teacher == teacher_user
    assert grade.score == 85

    expected_str = f'{submission} graded 85/100 by {teacher_user}'
    assert str(grade) == expected_str


@pytest.mark.django_db
def test_grade_score_validation(submission, teacher_user):
    with pytest.raises(ValueError):
        Grade.objects.create(submission=submission, teacher=teacher_user, score=-1)

    with pytest.raises(ValueError):
        Grade.objects.create(submission=submission, teacher=teacher_user, score=101)


@pytest.mark.django_db
def test_grade_one_to_one_constraint(submission, teacher_user):
    Grade.objects.create(submission=submission, teacher=teacher_user, score=90)

    with pytest.raises(Exception):
        Grade.objects.create(submission=submission, teacher=teacher_user, score=95)
