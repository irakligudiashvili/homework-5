from rest_framework import serializers
from api.models import Course
from .lecture import LectureSerializer
from .user import UserSerializer
from ..services.course import CourseService


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner']
        read_only_fields = ['id', 'email', 'role']

    def create(self, validated_data):
        owner = self.context['request'].user

        return CourseService.create_course(owner, validated_data)


class CourseDetailSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)
    teachers = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'owner',
            'lectures',
            'teachers',
            'students'
        ]
        read_only_fields = [
            'id',
            'lectures',
            'teachers',
            'students'
        ]

    def get_teachers(self, obj):
        enrollments = obj.enrollments.filter(user__role__iexact='teacher')
        return UserSerializer([e.user for e in enrollments], many=True).data

    def get_students(self, obj):
        enrollments = obj.enrollments.filter(user__role__iexact='student')
        return UserSerializer([e.user for e in enrollments], many=True).data
