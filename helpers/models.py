from django.contrib.auth.models import User
from django.db import models
from rules.contrib.models import RulesModelBase, RulesModelMixin

from helpers.utils import to_jalali_datetime


class BaseModelManager(models.Manager):
    def deleted(self):
        return self.filter(is_deleted=True)

    def not_deleted(self):
        return self.filter(is_deleted=False)


class BaseModel(RulesModelMixin, models.Model, metaclass=RulesModelBase):
    created_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_created_by_user",
        related_query_name="%(app_label)s_%(class)s_created_by_user",
        on_delete=models.CASCADE,
        null=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_updated_by_user",
        related_query_name="%(app_label)s_%(class)s_updated_by_user",
        on_delete=models.CASCADE,
        null=True
    )
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    auto_cols = [
        'created_by',
        'updated_by',
        'create_time',
        'modify_time',
        'is_deleted',
        'modify_time_formatted',
        'create_time_formatted',
        'modify_date_formatted',
        'create_date_formatted',
    ]

    objects = BaseModelManager()

    @property
    def modify_time_formatted(self):
        return to_jalali_datetime(self.modify_time).strftime("%d %b %Y %H:%M")

    @property
    def create_time_formatted(self):
        return to_jalali_datetime(self.create_time).strftime("%d %b %Y %H:%M")

    @property
    def modify_date_formatted(self):
        return to_jalali_datetime(self.modify_time).strftime("%d %b %Y")

    @property
    def create_date_formatted(self):
        return to_jalali_datetime(self.create_time).strftime("%d %b %Y")

    @classmethod
    def from_dict(cls, prop_dict):
        assert isinstance(prop_dict, dict)

        rtn = cls()
        for key, value in prop_dict.items():
            if key in cls.auto_cols:
                continue
            setattr(rtn, key, value)

        return rtn

    class Meta:
        ordering = ('-modify_time',)
        abstract = True
