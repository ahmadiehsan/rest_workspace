from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from helpers.models import BaseModel


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    text = models.TextField(verbose_name=_('text'))
    model_type = models.CharField(max_length=50, verbose_name=_('model_type'))
    model_id = models.CharField(max_length=50, verbose_name=_('model_id'))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_set',
        related_query_name='child',
        verbose_name=_('parent')
    )

    def __str__(self):
        return '{}, {}, {}'.format(self.user, self.model_type, self.model_id)
