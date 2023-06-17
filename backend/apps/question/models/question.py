from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from apps.common.dataclass import Badge
from apps.common.models import TimestampUserMixin
from apps.question.models.choice import Choice
from apps.question.models.comment import Comment
from apps.user.models import User


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

    def get_badge(self, user: User | AnonymousUser) -> Badge | None:
        """
        問題のバッジを取得する。

        Returns:
            Badge | None: 問題のバッジ
        """
        badge_class = [
            'me-2',
        ]
        if timezone.now() - self.created_at < timedelta(days=1):
            return Badge(
                label='新着',
                color='#f1556c',
                add_class=badge_class,
            )
        if user.is_authenticated and not user.get_history(self.pk).exists():
            return Badge(
                label='未解答',
                color='#1abc9c',
                add_class=badge_class,
            )
        return None

    def get_ai_comment(self) -> Comment | None:
        """
        問題のAIコメントを取得する。

        Returns:
            Comment | None: Comment オブジェクト
        """
        comment_qs = self.get_comments()
        ai_comment = comment_qs.filter(comment_type=Comment.CommentType.AI_COMMENT).first()
        return ai_comment

    def get_chat_comments(self) -> QuerySet[Comment]:
        """
        問題のチャットコメントを取得する。

        Returns:
            QuerySet[Comment]: コメントのQuerySet
        """
        comment_qs = self.get_comments()
        chat_comments = comment_qs.filter(comment_type=Comment.CommentType.CHAT_COMMENT).order_by('-created_at')
        return chat_comments
