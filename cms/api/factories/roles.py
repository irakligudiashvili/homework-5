class UserRoleFactory:
    STUDENT = 'student'
    TEACHER = 'teacher'

    _roles = {
        STUDENT: 'Student',
        TEACHER: 'Teacher'
    }

    @classmethod
    def choices(cls):
        return [(key, label) for key, label in cls._roles.items()]

    @classmethod
    def labels(cls):
        return list(cls._roles.values())

    @classmethod
    def is_valid(cls, role):
        return role in cls._roles
