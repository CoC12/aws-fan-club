from django.db import models

from apps.common.models import TimestampUserMixin
from apps.question.models.choice import Choice
from apps.question.models.comment import Comment


class Question(TimestampUserMixin):
    """
    問題モデル
    """

    class Meta:
        """
        Metaクラス
        """
        verbose_name = '問題'
        verbose_name_plural = '問題一覧'

    text = models.TextField(
        verbose_name='問題文',
    )

    explanation = models.TextField(
        verbose_name='解説',
        blank=True,
    )

    def get_choices(self) -> models.QuerySet[Choice]:
        """
        問題の選択肢を取得する。

        Returns:
            models.QuerySet[Choice]: 選択肢のQuerySet
        """
        return self.choices.order_by('number')

    def get_comments(self) -> models.QuerySet[Comment]:
        """
        問題のコメントを取得する。

        Returns:
            models.QuerySet[Comment]: コメントのQuerySet
        """
        return self.comments.order_by('-created_at')
