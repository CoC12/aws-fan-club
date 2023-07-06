from django.db import models

from apps.common.models import TimestampUserMixin
from apps.user.models import User


class Comment(TimestampUserMixin):
    """
    コメントモデル
    """

    class Meta:
        """
        Metaクラス
        """
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント一覧'

    class CommentType(models.IntegerChoices):
        """
        コメント種別
        """
        AI_COMMENT = (1, 'AIコメント')
        QUERY_COMMENT = (2, '質問コメント')
        CHAT_COMMENT = (3, '雑談コメント')

    question = models.ForeignKey(
        'question.Question',  # 循環参照回避のため、文字列で参照
        verbose_name='問題',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    title = models.CharField(
        'タイトル',
        blank=True,
        max_length=256,
    )
    comment = models.TextField(
        'コメント',
    )
    comment_type = models.IntegerField(
        'コメント種別',
        choices=CommentType.choices,
    )
    commented_by = models.ForeignKey(
        User,
        verbose_name='コメント者',
        on_delete=models.CASCADE,
    )
