from django.db import models
from api.models import Course


class Lecture(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lectures'
    )
    topic = models.CharField(max_length=255)
    file = models.FileField(upload_to='lectures/')

    def __str__(self):
        return self.topic
