from rest_framework import serializers
from api.models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'course', 'topic', 'file', 'assignments']
        read_only_fields = ['id', 'assignments']
