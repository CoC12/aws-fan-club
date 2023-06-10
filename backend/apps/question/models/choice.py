from django.db import models

from apps.common.models import TimestampUserMixin


class Choice(TimestampUserMixin):
    """
    選択肢モデル
    """

    class Meta:
        """
        Metaクラス
        """
        verbose_name = '選択肢'
        verbose_name_plural = '選択肢一覧'
        ordering = ['question', 'number']
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'number'],
                name='unique_choice',
            ),
        ]

    question = models.ForeignKey(
        'question.Question',  # 循環参照回避のため、文字列で参照
        verbose_name='問題',
        on_delete=models.CASCADE,
        related_name='choices',
    )

    number = models.PositiveSmallIntegerField(
        verbose_name='選択肢番号',
    )

    choice_text = models.TextField(
        verbose_name='選択肢文章',
    )

    is_answer = models.BooleanField(
        verbose_name='正解か',
        default=False,
    )
