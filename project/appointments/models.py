from django.db import models
from datetime import datetime


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    subscriber_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.subscriber_name}: {self.message}'

