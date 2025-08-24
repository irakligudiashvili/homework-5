import pytest
from api.serializers import UserSerializer, UserRegistrationSerializer


@pytest.mark.django_db
def test_user_serializer_serialization(teacher_user):
    serializer = UserSerializer(teacher_user)
    data = serializer.data

    assert data['id'] == teacher_user.id
    assert data['first_name'] == teacher_user.first_name
    assert data['last_name'] == teacher_user.last_name
    assert data['email'] == teacher_user.email
    assert data['role'] == teacher_user.role


@pytest.mark.django_db
def test_user_registration_serializer_creation():
    payload = {
        'first_name': 'Alice',
        'last_name': 'Wonder',
        'email': 'alice@example.com',
        'password': 'supersecret',
        'role': 'student'
    }

    serializer = UserRegistrationSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()
    assert user.id is not None
    assert user.first_name == 'Alice'
    assert user.last_name == 'Wonder'
    assert user.email == 'alice@example.com'
    assert user.role == 'student'
    assert user.check_password('supersecret')


@pytest.mark.django_db
def test_user_registration_serializer_invalid_role():
    payload = {
        'first_name': 'Bob',
        'last_name': 'Builder',
        'email': 'bob@example.com',
        'password': 'password123',
        'role': 'invalid_role'
    }

    serializer = UserRegistrationSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'role' in serializer.errors


@pytest.mark.django_db
def test_user_serializer_read_only_fields(student_user):
    serializer = UserSerializer(student_user)
    data = serializer.data

    assert 'id' in serializer.fields
    assert serializer.fields['id'].read_only
    assert 'email' in serializer.fields
    assert serializer.fields['email'].read_only
    assert 'role' in serializer.fields
    assert serializer.fields['role'].read_only
