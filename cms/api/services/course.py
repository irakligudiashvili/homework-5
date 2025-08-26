from api.models import Course, Enrollment


class CourseService:
    @staticmethod
    def create_course(owner, validated_data):
        if owner.role.lower() != 'teacher':
            raise ValueError('Only teachers can own courses')

        course = Course.objects.create(owner=owner, **validated_data)
        Enrollment.objects.get_or_create(user=owner, course=course)

        return course
