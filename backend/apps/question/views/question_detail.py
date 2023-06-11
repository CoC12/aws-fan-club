import typing

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from apps.common.dataclass import Button
from apps.common.views import BaseView, BreadcrumbItem
from apps.question.models import Question
from config.sidebar_config import SidebarConfig


class QuestionDetail(BaseView):
    """
    問題詳細画面
    """
    template_name = 'question_detail.html'
    sidebar_items = SidebarConfig.questions

    def get(self, request: HttpRequest, *args: typing.Any, **kwargs: typing.Any) -> HttpResponse:
        """
        Get メソッド

        Args:
            request (HttpRequest): HttpRequest オブジェクト

        Returns:
            HttpResponse: HttpResponse オブジェクト
        """
        try:
            response = super().get(request, *args, **kwargs)
        except Question.DoesNotExist:
            pk = self.kwargs['pk']
            redirect_url = reverse('question_list')
            messages.error(request, f'問題ID「{pk}」の問題が存在しません。')
            return HttpResponseRedirect(redirect_url)
        return response

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        """
        コンテキストデータを返す。

        Returns:
            dict[str, typing.Any]: コンテキストデータ
        """
        pk = self.kwargs['pk']
        question = Question.objects.prefetch_related('choices').get(pk=pk)

        context = super().get_context_data(**kwargs)
        context.update({
            'card_title': f'問題: {pk}',
            'question': question,
            'button': Button(
                label='決定',
                add_class=[
                    'js-question-card__confirm-button',
                ],
            ),
        })
        return context

    def _get_breadcrumb_items(self) -> list[BreadcrumbItem]:
        """
        パンくずリストに表示する項目を返す。

        Returns:
            list[BreadcrumbItem]: パンくずリストに表示する項目
        """
        pk = self.kwargs['pk']

        breadcrumb_items: list[BreadcrumbItem] = [
            {
                'label': 'トップページ',
                'href': reverse('top_page'),
            },
            {
                'label': '問題一覧',
                'href': reverse('question_list'),
            },
            {
                'label': f'問題「{pk}」',
            },
        ]
        return breadcrumb_items
