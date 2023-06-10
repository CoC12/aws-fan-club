from django.contrib.auth.models import AbstractUser

from apps.common.models import TimestampUserMixin


class User(AbstractUser, TimestampUserMixin):
    """
    Userモデル
    """
