from rest_framework import serializers
from api.models import Submission, Assignment
from api.services.submission import SubmissionService


class SubmissionSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all()
    )

    class Meta:
        model = Submission
        fields = ['id', 'user', 'assignment', 'file']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user

        return SubmissionService.create_submission(user, validated_data)
