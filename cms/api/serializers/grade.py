from rest_framework import serializers
from api.models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'submission', 'teacher', 'score']
        read_only_fields = ['id', 'teacher']

    def validate_score(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError(
                'Score must be between 0 and 100'
            )

        return value
