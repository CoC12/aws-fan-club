from django.db import models

from apps.question.models import Choice, Question


class History(models.Model):
    """
    解答履歴モデル
    """

    class Meta:
        """
        Metaクラス
        """
        verbose_name = '解答履歴'
        verbose_name_plural = '解答履歴一覧'

    user = models.ForeignKey(
        'user.User',  # 循環参照回避のため、文字列で参照
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    choices = models.ManyToManyField(
        Choice,
        verbose_name='解答',
        related_name='choices',
    )
