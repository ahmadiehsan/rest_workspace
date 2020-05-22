import jdatetime
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError


def to_jalali_datetime(datetime):
    """convert gregorian datetime to jalali date time"""
    return jdatetime.datetime.fromgregorian(datetime=datetime)


def clean_phone_number(phone_number):
    """add +98 to start of phone number"""

    input_phone_len = len(phone_number)

    if input_phone_len >= 10 or input_phone_len <= 13:
        if input_phone_len == 13:
            if phone_number[0] == '+':
                return phone_number
            raise ValidationError(_('please enter a valid phone number'))

        elif input_phone_len == 12:
            if phone_number[0:2] == '98':
                return '+' + phone_number
            raise ValidationError(_('please enter a valid phone number'))

        elif input_phone_len == 11:
            if phone_number[0] == '0':
                return '+98' + phone_number[1:]
            raise ValidationError(_('please enter a valid phone number'))

        elif input_phone_len == 10:
            if phone_number[0] == '9':
                return '+98' + phone_number
            raise ValidationError(_('please enter a valid phone number'))

    raise ValidationError(_('please enter a valid phone number'))


class classproperty(property):
    def __get__(self, obj, obj_type=None):
        return super(classproperty, self).__get__(obj_type)

    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))
