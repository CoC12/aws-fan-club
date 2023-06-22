import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet

from apps.common.models import TimestampUserMixin
from apps.common.validators import CharsValidatorBuilder, ValidatorPattern

from . import History

# アカウントID のバリデーターを生成する
validator_builder = CharsValidatorBuilder()
validator_builder.add_pattern(
    ValidatorPattern.UPPERCASE,
    ValidatorPattern.LOWERCASE,
    ValidatorPattern.DIGITS,
    ValidatorPattern.UNDERSCORE,
)
account_id_validator = validator_builder.build()


def generate_account_id() -> str:
    """
    アカウントID を生成する。

    TODO: いつかはかぶるかもしれないので、実装見直し

    Returns:
        str: アカウントID
    """
    return uuid.uuid4().hex[:16]


class User(AbstractUser, TimestampUserMixin):
    """
    Userモデル
    """
    account_id = models.CharField(
        verbose_name='アカウントID',
        max_length=16,
        unique=True,
        db_index=True,
        validators=[
            account_id_validator,
        ],
        default=generate_account_id,
    )
    profile_image = models.ImageField(
        verbose_name='プロフィール画像',
        upload_to='profile_image/',
        default='profile_image/user-default.png',
    )
    bio = models.TextField(
        verbose_name='自己紹介',
        max_length=1000,
        blank=True,
    )

    def get_histories(self) -> QuerySet[History]:
        """
        ユーザーの解答履歴一覧を取得する。

        Returns:
            QuerySet[History]: 解答履歴一覧
        """
        return self.histories.all()

    def get_history(self, question_id: int) -> QuerySet[History]:
        """
        ユーザーの指定した問題の解答履歴一覧を取得する。

        Args:
            question_id (int): 問題ID

        Returns:
            QuerySet[History]: 解答履歴一覧
        """
        return self.histories.filter(
            question_id=question_id,
        )
