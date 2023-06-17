import typing

from django.urls import reverse, reverse_lazy

from apps.common.dataclass import Row, Table
from apps.common.services import PaginationService
from apps.common.utils import to_human_readable_datetime
from apps.common.views import BaseView, BreadcrumbItem
from apps.question.models import Question
from config.sidebar_config import SidebarConfig


class QuestionList(BaseView):
    """
    問題一覧画面
    """
    template_name = 'question_list.html'
    sidebar_items = SidebarConfig.questions

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        """
        コンテキストデータを返す。

        Returns:
            dict[str, typing.Any]: コンテキストデータ
        """
        question_list = self._get_question_list()

        pagination_service: PaginationService[Row] = PaginationService()
        current_page = pagination_service.get_current_page(self.request.GET)
        page_obj, page_range = pagination_service.get_page_object(question_list, current_page)

        context = super().get_context_data(**kwargs)
        context.update({
            'question_list_table': Table(
                page_obj=page_obj,
                page_range=page_range,
                headers=['ID', '問題文', '作成者', '作成日時', '最終更新日時'],
                html_safe_headers=['問題文'],
                empty_text='表示するデータがありません。',
            ),
        })
        return context

    def _get_question_list(self) -> list[Row]:
        """
        テーブル表示用の問題一覧を返す。

        Returns:
            list[Row]: テーブル表示用の問題一覧
        """
        question_qs = Question.objects.order_by('-created_at')
        question_list = [
            Row(
                href=reverse('question_detail', kwargs={'pk': question.pk}),
                data={
                    'ID': str(question.pk),
                    '問題文': self._build_question_text_html(question),
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
