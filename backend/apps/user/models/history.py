from django.db import models


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
        related_name='histories',
    )
    question = models.ForeignKey(
        'question.Question',  # 循環参照回避のため、文字列で参照
        on_delete=models.CASCADE,
    )
    choices = models.ManyToManyField(
        'question.Choice',  # 循環参照回避のため、文字列で参照
        verbose_name='解答',
        related_name='choices',
    )
