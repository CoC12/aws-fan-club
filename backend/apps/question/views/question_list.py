import typing
from collections.abc import Callable
from dataclasses import dataclass

from django.db.models import Q
from django.urls import reverse, reverse_lazy

from apps.common.dataclass import RadioButton, RadioGroup, Row, Table
from apps.common.services import PaginationService
from apps.common.utils import to_human_readable_datetime
from apps.common.views import BaseView, BreadcrumbItem
from apps.question.models import Question
from apps.user.models import User
from config.sidebar_config import SidebarConfig


@dataclass
class QuestionListFilter:
    """
    問題一覧検索フィルター
    """
    label: str
    filter_query: Callable[[User], Q] = lambda user: Q()
    exclude_query: Callable[[User], Q] = lambda user: Q()


class QuestionList(BaseView):
    """
    問題一覧画面
    """
    template_name = 'question_list.html'
    sidebar_items = SidebarConfig.questions

    available_filters = {
        'all': QuestionListFilter('すべて'),
        'unsolved': QuestionListFilter(
            '未解答の問題',
            exclude_query=lambda user: Q(history__user=user),
        ),
        'good': QuestionListFilter(
            'いいねした問題',
            filter_query=lambda user: Q(feedbacks__user=user, feedbacks__rating=1),
        ),
        'commented': QuestionListFilter(
            'コメントした問題',
            filter_query=lambda user: Q(comments__commented_by=user),
        ),
    }

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        """
        コンテキストデータを返す。

        Returns:
            dict[str, typing.Any]: コンテキストデータ
        """
        filter_key = self.request.GET.get('filter')
        if filter_key not in self.available_filters.keys():
            filter_key = 'all'

        question_list = self._get_question_list(filter_key=filter_key)

        pagination_service: PaginationService[Row] = PaginationService()
        current_page = pagination_service.get_current_page(self.request.GET)
        page_obj, page_range = pagination_service.get_page_object(question_list, current_page)

        context = super().get_context_data(**kwargs)
        context.update({
            'question_list_table': Table(
                page_obj=page_obj,
                page_range=page_range,
                headers=['ID', 'カテゴリ', '問題文', 'コメント数', '作成者', '作成日時', '最終更新日時'],
                html_safe_headers=['問題文', 'コメント数'],
                body_only_headers=['コメント数'],
                empty_text='表示するデータがありません。',
            ),
        })

        if self.request.user.is_authenticated:
            context.update({
                'search_radio_group': RadioGroup(
                    name='search_radio_group',
                    add_class=['js-question-list-table__search_radio_group'],
                    radio_button_list=[
                        RadioButton(
                            html_id=f'id-question-list__search-radio-{key}',
                            value=key,
                            label=question_filter.label,
                            selected=(filter_key == key),
                        ) for key, question_filter in self.available_filters.items()
                    ],
                ),
            })
        return context

    def _get_question_list(self, filter_key: str) -> list[Row]:
        """
        テーブル表示用の問題一覧を返す。

        Args:
            filter_key (str): フィルタするキー

        Returns:
            list[Row]: テーブル表示用の問題一覧
        """
        filter_query = Q()
        exclude_query = Q()

        user = self.request.user
        if user.is_authenticated:
            question_filter = self.available_filters[filter_key]
            filter_query = question_filter.filter_query(user)
            exclude_query = question_filter.exclude_query(user)

        question_qs = Question.objects.filter(filter_query).exclude(exclude_query).distinct('pk').order_by('-pk')
        question_list = [
            Row(
                href=reverse('question_detail', kwargs={'pk': question.pk}),
                data={
                    'ID': str(question.pk),
                    'カテゴリ': question.get_category_display() or '未設定',
                    '問題文': self._build_question_text_html(question),
                    'コメント数': self._build_comment_count_html(question),
                    '作成者': question.created_by,
                    '作成日時': to_human_readable_datetime(question.created_at),
                    '最終更新日時': to_human_readable_datetime(question.updated_at),
                },
            ) for question in question_qs
        ]
        return question_list

    def _build_question_text_html(self, question: Question) -> str:
        """
        問題テキストのHTML文字列を取得する。

        Args:
            question (Question): Question オブジェクト

        Returns:
            str: 問題テキストのHTML文字列
        """
        badge = question.get_badge(self.request.user)
        if badge is None:
            return question.text
        return f'{badge}{question.text}'

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

    def _get_breadcrumb_items(self) -> list[BreadcrumbItem]:
        """
        パンくずリストに表示する項目を返す。

        Returns:
            list[BreadcrumbItem]: パンくずリストに表示する項目
        """
        breadcrumb_items: list[BreadcrumbItem] = [
            {
                'label': 'トップページ',
                'href': reverse_lazy('top_page'),
            },
            {
                'label': '問題一覧',
            },
        ]
        return breadcrumb_items
