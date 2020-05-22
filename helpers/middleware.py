from threading import local

import jwt
from django.db.models import signals
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import curry
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.settings import api_settings

try:
    from django.contrib.auth import get_user_model
except ImportError:  # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

_user = local()


class WhoDidMiddleware(MiddlewareMixin):
    """
    automatically fill created_by and modify_by fields
    """

    @staticmethod
    def is_meta_has_this_field(fields, field_name):
        for field_item in fields:
            if field_item.name == field_name:
                return True
        return False

    @staticmethod
    def has_created_by(instance):
        if not instance.created_by:
            return False
        return True

    def mark_who_did(self, user, sender, instance, **kwargs):
        if self.is_meta_has_this_field(instance._meta.fields, 'created_by') and \
                not self.has_created_by(instance):
            instance.created_by = user

        if self.is_meta_has_this_field(instance._meta.fields, 'updated_by'):
            instance.updated_by = user

    def process_request(self, request):
        if request.method not in ('HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user
            else:
                user = self.get_user_from_auth_header(request)
                if user is not None:
                    request.user = user

            _user.value = user

            mark_who_did = curry(self.mark_who_did, _user.value)
            signals.pre_save.connect(
                mark_who_did,
                dispatch_uid=(self.__class__, request,),
                weak=False
            )

    def get_user_from_auth_header(self, request):
        try:
            auth_keyword, token = get_authorization_header(request).split()
            jwt_header, claims, signature = str(token).split('.')

            try:
                payload = api_settings.JWT_DECODE_HANDLER(token)
                try:
                    user_id = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER(payload)

                    if user_id:
                        user = User.objects.get(pk=user_id, is_active=True)
                        return user
                    else:
                        msg = 'Invalid payload'
                        return None
                except User.DoesNotExist:
                    msg = 'Invalid signature'
                    return None

            except jwt.ExpiredSignature:
                msg = 'Signature has expired.'
                return None
            except jwt.DecodeError:
                msg = 'Error decoding signature.'
                return None
        except ValueError:
            return None

    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid=(self.__class__, request,))
        return response
