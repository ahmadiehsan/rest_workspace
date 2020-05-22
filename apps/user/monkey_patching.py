from django.contrib.auth import get_user_model


@property
def is_vip(self):
    try:
        return self.vip_data.is_active
    except Exception:
        return False


UserModel = get_user_model()
UserModel.add_to_class('is_vip', is_vip)
