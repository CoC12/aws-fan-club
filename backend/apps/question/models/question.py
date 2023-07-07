from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import Count, QuerySet
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

    class Category(models.IntegerChoices):
        """
        カテゴリー
        """
        # AWSクラウドの概念
        AWS_ADVANTAGES = (1, 'AWSの長所・利点')
        CLOUD_ARCHITECTURE_PRINCIPLES = (2, 'クラウドアーキテクチャの設計原理')
        AWS_WELL_ARCHITECTED_FRAMEWORK = (3, 'AWS Well-Architected フレームワーク')
        # AWSのセキュリティ
        SHARED_RESPONSIBILITY_MODEL = (4, '責任共有モデル')
        AWS_CLOUD_SECURITY = (5, 'AWSクラウドのセキュリティ')
        IAM = (6, 'IAM')
        SECURITY_GROUPS = (7, 'セキュリティグループ')
        AWS_SHIELD_AND_WAF = (8, 'AWS Shield と AWS WAF')
        AMAZON_INSPECTOR = (9, 'Amazon Inspector')
        # AWSのテクノロジー
        GLOBAL_INFRASTRUCTURE = (10, 'グローバルインフラストラクチャ')
        # コンピューティングサービス
        EC2 = (11, 'EC2')
        ELB = (12, 'ELB')
        AUTO_SCALING = (13, 'Auto Scaling')
        AWS_LAMBDA = (14, 'AWS Lambda')
        # ストレージサービス
        EBS = (15, 'EBS')
        S3 = (16, 'S3')
        # ネットワークサービス
        VPC = (17, 'VPC')
        AMAZON_CLOUDFRONT = (18, 'Amazon CloudFront')
        ROUTE_53 = (19, 'Route 53')
        # データベースサービス
        RDS = (20, 'RDS')
        DYNAMODB = (21, 'DynamoDB')
        # 管理サービス
        AMAZON_CLOUDWATCH = (22, 'Amazon CloudWatch')
        AWS_TRUSTED_ADVISOR = (23, 'AWS Trusted Advisor')
        # 請求と料金
        AWS_PRICING_MODEL = (24, 'AWS料金モデル')
        BILLING_DASHBOARD = (25, '請求ダッシュボード')
        MULTI_ACCOUNT_OPERATION = (26, 'マルチアカウントの運用')
        AWS_SUPPORT_PLANS = (27, 'AWSのサポートプラン')

    text = models.TextField(
        verbose_name='問題文',
    )

    explanation = models.TextField(
        verbose_name='解説',
        blank=True,
    )

    category = models.IntegerField(
        verbose_name='カテゴリー',
        choices=Category.choices,
        null=True,
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

    def get_feedbacks(self) -> dict[str, int]:
        """
        問題のフィードバックの集計を取得する。

        Returns:
            dict[str, int]: 問題のフィードバックの集計
                {
                    'good': 12,
                    'bad': 3,
                }
        """
        feedback_dict = {
            'good': 0,
            'bad': 0,
        }

        feedback_by_rating = self.feedbacks.values('rating').annotate(count=Count('id'))
        for feedback in feedback_by_rating:
            if feedback['rating'] == 1:
                feedback_dict['good'] = feedback['count']
            elif feedback['rating'] == 0:
                feedback_dict['bad'] = feedback['count']
        return feedback_dict

    def get_user_feedback(self, user: User | AnonymousUser) -> int | None:
        """
        ユーザーに紐づく、問題のフィードバックを取得する。

        Returns:
            int | None: 問題のフィードバック 0 or 1 or None
        """
        if user.is_authenticated:
            feedback = self.feedbacks.filter(user=user).first()
            if feedback:
                return feedback.rating
        return None
