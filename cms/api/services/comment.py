from api.models import Comment


class CommentService:
    @staticmethod
    def create_comment(user, validated_data):
        validated_data['user'] = user
        comment = Comment.objects.create(**validated_data)

        return comment
