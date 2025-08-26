from rest_framework import serializers
from api.models import Comment
from api.services import CommentService


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'submission', 'user', 'content']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user

        return CommentService.create_comment(user, validated_data)
