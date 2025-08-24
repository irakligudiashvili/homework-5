from django.db import models
from django.conf import settings


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} enrolled in {self.course}'
