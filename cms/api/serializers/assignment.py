from rest_framework import serializers
from api.models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']
