import typing

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from apps.common.dataclass import Avatar, Button
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
        previous_question, current_question, next_question = self._get_questions()

        if current_question is None:
            raise Question.DoesNotExist

        context = super().get_context_data(**kwargs)
        context.update({
            'question_card_title': f'問題: {current_question.pk}',
            'question_comment_card_title': 'コメント',
            'question': current_question,
            'question_badge': current_question.get_badge(self.request.user),
            'confirm_button': Button(
                label='決定',
                add_class=[
                    'js-question-card__confirm-button',
                ],
            ),
            'ai_comment_button': Button(
                label='生成',
                secondary=True,
                add_class=[
                    'js-question-card__ai-comment-button',
                    'border',
                    'border-secondary',
                ],
            ),
            'previous_page_button': Button(
                label='前の問題',
                link=reverse('question_detail', kwargs={'pk': previous_question.pk}) if previous_question else '',
                disabled=previous_question is None,
            ),
            'next_page_button': Button(
                label='次の問題',
                link=reverse('question_detail', kwargs={'pk': next_question.pk}) if next_question else '',
                disabled=next_question is None,
            ),
            # TODO ユーザーに紐づいたアイコンにする
            'avatar': Avatar(
                static_src='images/user-default.png',
                alt='user icon',
            ),
        })
        return context

    def _get_questions(self) -> tuple[Question | None, Question | None, Question | None]:
        """
        現在、直前、直後のページの問題を取得する。

        Returns:
            tuple[Question | None, Question | None, Question | None]: 現在、直前、直後のページの問題
        """
        pk = self.kwargs['pk']

        base_qs = Question.objects.prefetch_related('choices')
        previous_qs = base_qs.filter(pk__lte=pk).order_by('-pk')[:2]  # 直前の pk の QuerySet（該当の pk を含む）
        next_ps = base_qs.filter(pk__gt=pk).order_by('pk')[:1]  # 直後の pk の QuerySet
        question_qs = previous_qs.union(next_ps)

        previous_question = None
        current_question = None
        next_question = None

        for question in question_qs:
            if question.pk == pk:
                current_question = question
                continue
            if question.pk < pk:
                previous_question = question
                continue
            if question.pk > pk:
                next_question = question

        return previous_question, current_question, next_question

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
