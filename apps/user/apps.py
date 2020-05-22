from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.user'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from apps.user import monkey_patching
