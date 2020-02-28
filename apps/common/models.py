from django.contrib.auth.models import User
from django.db import models

from helpers.models import BaseModel


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    model_type = models.CharField(max_length=50)
    model_id = models.CharField(max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_set',
        related_query_name='child'
    )

    def __str__(self):
        return '{}, {}, {}'.format(self.user, self.model_type, self.model_id)
