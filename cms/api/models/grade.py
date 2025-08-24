from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

from .submission import Submission


class Grade(models.Model):
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='grade'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='graded_submissions',
        limit_choices_to={'role': 'teacher'}
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def save(self, *args, **kwargs):
        if not (0 <= self.score <= 100):
            raise ValueError('Score must be between 0 and 100')

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.submission} graded {self.score}/100 by {self.teacher}'
