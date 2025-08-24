import pytest
from api.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email='user@example.com',
        password='pass123',
        first_name='John',
        last_name='Doe',
        role='student'
    )

    assert user.id is not None
    assert user.email == 'user@example.com'
    assert user.first_name == 'John'
    assert user.role == 'student'
    assert user.check_password('pass123')
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_user_without_email_raises():
    with pytest.raises(ValueError) as exc:
        User.objects.create_user(email=None, password='123', role='teacher')
    assert 'Email is required' in str(exc.value)


@pytest.mark.django_db
def test_create_user_without_role_raises():
    with pytest.raises(ValueError) as exc:
        User.objects.create_user(email='test@example.com', password='123')
    assert 'Role is required' in str(exc.value)


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        email='admin@example.com',
        password='adminpass',
        first_name='Admin',
        last_name='User',
        role='teacher'
    )

    assert user.id is not None
    assert user.is_staff
    assert user.is_superuser
    assert user.check_password('adminpass')
