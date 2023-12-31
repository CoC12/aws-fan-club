import logging
import os
import typing

from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


def create_superuser(*args: typing.Any, **kwargs: typing.Any) -> None:
    """
    初期スーパーユーザー作成
    """
    User = get_user_model()
    username = os.environ.get('SUPERUSER_NAME')
    password = os.environ.get('SUPERUSER_PASSWORD')
    if username and password:
        if User.objects.filter(username=username).exists():
            logger.info('Skip creation since there is already a superuser with the same name')
        else:
            User.objects.create_superuser(
                username=username,
                email=None,
                password=password,
                is_superuser=True,
                is_staff=True,
                is_active=True,
            )


def create_chat_gpt_user(*args: typing.Any, **kwargs: typing.Any) -> None:
    """
    ChatGPT用ユーザー作成
    """
    User = get_user_model()
    username = 'ChatGPT'
    password = None
    if User.objects.filter(username=username).exists():
        logger.info('Skip creation since there is already a ChatGPT user')
        return
    User.objects.create_user(
        username=username,
        email=None,
        password=password,
        is_superuser=False,
        is_staff=False,
        is_active=False,
    )
