from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet

from apps.common.models import TimestampUserMixin

from . import History


class User(AbstractUser, TimestampUserMixin):
    """
    Userモデル
    """

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
