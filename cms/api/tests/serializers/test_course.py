import pytest
from api.models import Course, Lecture, Enrollment
from api.serializers.course import CourseSerializer, CourseDetailSerializer


@pytest.mark.django_db
def test_course_serializer_basic(teacher_user):
    course = Course.objects.create(
        title="Test Course",
        description="Course description",
        owner=teacher_user
    )

    serializer = CourseSerializer(course)
    data = serializer.data

    assert data['id'] == course.id
    assert data['title'] == "Test Course"
    assert data['description'] == "Course description"
    assert data['owner'] == str(teacher_user)


@pytest.mark.django_db
def test_course_detail_serializer_nested(course, teacher_user, student_user):
    Enrollment.objects.create(user=teacher_user, course=course)
    Enrollment.objects.create(user=student_user, course=course)

    lecture1 = Lecture.objects.create(course=course, topic="Lecture 1", file="lectures/file1.pdf")
    lecture2 = Lecture.objects.create(course=course, topic="Lecture 2", file="lectures/file2.pdf")

    serializer = CourseDetailSerializer(course)
    data = serializer.data

    assert data['id'] == course.id
    assert data['lectures'][0]['topic'] == "Lecture 1"
    assert data['lectures'][1]['topic'] == "Lecture 2"

    teacher_emails = [t['email'] for t in data['teachers']]
    student_emails = [s['email'] for s in data['students']]

    assert teacher_user.email in teacher_emails
    assert student_user.email in student_emails
