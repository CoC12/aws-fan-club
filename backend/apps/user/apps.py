from django.apps import AppConfig
from django.db.models.signals import post_migrate

from apps.user.signals import create_chat_gpt_user, create_superuser


class UserConfig(AppConfig):
    """
    User app config
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'

    def ready(self) -> None:
        """Setup signal handlers."""
        post_migrate.connect(create_superuser, sender=self)
        post_migrate.connect(create_chat_gpt_user, sender=self)
