from api.models import Submission


class SubmissionService:
    @staticmethod
    def create_submission(user, validated_data):
        validated_data['user'] = user
        submission = Submission.objects.create(**validated_data)

        return submission
