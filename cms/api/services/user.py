from api.models import User


class UserService:
    @staticmethod
    def create_user(validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
