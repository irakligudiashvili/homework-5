from django.conf import settings
from django.db import models

from .submission import Submission


class Comment(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()

    def __str__(self):
        return (
            f'Comment by {self.user.email} on submission {self.submission.id}'
        )
