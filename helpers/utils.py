from django.utils.translation import ugettext as _

from rest_framework.exceptions import ValidationError


def clean_phone_number(phone_number):
    """add +98 to start of phone number"""

    cleaned_number = ''
    input_phone_len = len(phone_number)

    if input_phone_len >= 10 or input_phone_len <= 13:
        if input_phone_len == 13:
            if phone_number[0] == '+':
                cleaned_number = phone_number
                return cleaned_number
            raise ValidationError(_('please enter a valid phone number'))

        elif input_phone_len == 12:
            if phone_number[0:2] == '98':
                cleaned_number = '+' + phone_number
                return cleaned_number
            raise ValidationError(_('please enter a valid phone number'))

        elif input_phone_len == 11:
            if phone_number[0] == '0':
                cleaned_number = '+98' + phone_number[1:]
                return cleaned_number
            raise ValidationError(_('please enter a valid phone number'))

        elif input_phone_len == 10:
            if phone_number[0] == '9':
                cleaned_number = '0' + phone_number
                return cleaned_number
            raise ValidationError(_('please enter a valid phone number'))

    raise ValidationError(_('please enter a valid phone number'))
