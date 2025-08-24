from rest_framework import serializers
from api.models import Enrollment
from .user import UserSerializer
from .course import CourseSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course']
        read_only_fields = ['id']

    def validate(self, data):
        if Enrollment.objects.filter(
            user=data['user'],
            course=data['course']
        ).exists():
            raise serializers.ValidationError('User is already enrolled')

        return data
