from rest_framework.permissions import BasePermission

from api.models import Lecture, Course, Assignment, Submission, Enrollment


class IsEnrolled(BasePermission):
    @staticmethod
    def user_has_access(user, course):
        return Enrollment.objects.filter(
            user=user,
            course=course
        ).exists()

    def has_object_permission(self, request, view, obj):
        match obj:
            case Lecture():
                course = obj.course
            case Course():
                course = obj
            case Assignment():
                course = obj.lecture.course
            case Submission():
                course = obj.assignment.lecture.course
            case _:
                return False

        return self.user_has_access(request.user, course)
