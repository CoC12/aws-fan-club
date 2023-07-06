import typing

from django.urls import reverse

from apps.common.dataclass import Row, Table
from apps.common.services import PaginationService
from apps.common.views import BaseView
from apps.question.models import Comment, Question
from apps.user.models import History, User


class UserDetail(BaseView):
    """
    ユーザー詳細画面
    """
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        """
        コンテキストデータを返す。

        Returns:
            dict[str, typing.Any]: コンテキストデータ
        """
        account_id = self.kwargs['account_id']
        user = User.objects.get(account_id=account_id)

        pagination_service: PaginationService[Row] = PaginationService()

        question_list = self._get_good_feedback_question_list(user)
        current_page = pagination_service.get_current_page(self.request.GET)
        page_obj, page_range = pagination_service.get_page_object(question_list, current_page)

        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': f'{user.username} (@{user.account_id}) さん',
            'user': user,
            'count_list': {
                # TODO: 投稿機能作成後に対応
                'created_question': 0,
                'solved_question': History.objects.filter(user=user).count(),
                'comment': Comment.objects.filter(commented_by=user).count(),
            },
            'good_feedback_question_card_title': 'いいね した問題',
            'good_feedback_question_table': Table(
                page_obj=page_obj,
                page_range=page_range,
                headers=['ID', '問題文', 'コメント数', '作成者'],
                html_safe_headers=['問題文', 'コメント数'],
                body_only_headers=['コメント数'],
                empty_text='いいね した問題がありません。',
            ),
        })
        return context

    def _get_good_feedback_question_list(self, user: User) -> list[Row]:
        """
        テーブル表示用の「いいねした問題一覧」を返す。

        Args:
            user (User): User オブジェクト

        Returns:
            list[Row]: テーブル表示用の「いいねした問題一覧」
        """
        question_qs = Question.objects.filter(
            feedbacks__user=user,
            feedbacks__rating=1,
        ).order_by('-created_at')

        question_list = [
            Row(
                href=reverse('question_detail', kwargs={'pk': question.pk}),
                data={
                    'ID': str(question.pk),
                    '問題文': question.text,
                    'コメント数': self._build_comment_count_html(question),
                    '作成者': question.created_by,
                },
            ) for question in question_qs
        ]
        return question_list

    def _build_comment_count_html(self, question: Question) -> str:
        """
        コメント数のHTML文字列を取得する。

        Args:
            question (Question): Question オブジェクト

        Returns:
            str: コメント数のHTML文字列
        """
        count = len(question.get_chat_comments())
        if count == 0:
            return ''
        return f"""
            <div class="d-flex align-items-center">
                <span class="material-symbols-outlined fs-5">
                    chat_bubble
                </span>
                <span class="ms-1">
                    {count}
                </span>
            </div>
        """
