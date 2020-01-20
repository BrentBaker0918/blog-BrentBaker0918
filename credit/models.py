from django.conf import settings
from django.db import models

# Create your models here.
class CreditRating(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='credit_rating'
    )
    score = models.IntegerField()

    def __str__(self):
        return f'{self.user}: {self.score}'
