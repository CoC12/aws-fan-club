from django.apps import AppConfig


class QuestionConfig(AppConfig):
    """
    Question アプリケーションの Config
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.question'
