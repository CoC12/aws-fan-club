from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import TimestampUserMixin
from apps.user.models import User


class Feedback(TimestampUserMixin):
    """
    フィードバックモデル
    """

    class Meta:
        """
        Metaクラス
        """
        verbose_name = 'フィードバック'
        verbose_name_plural = 'フィードバック一覧'
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'user'],
                name='unique_question_user',
            ),
        ]

    question = models.ForeignKey(
        'question.Question',  # 循環参照回避のため、文字列で参照
        on_delete=models.CASCADE,
        related_name='feedbacks',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedbacks',
    )
    rating = models.IntegerField(
        'フィードバック',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
    )
