import typing

from django.http import HttpRequest, JsonResponse
from django.views.generic import View

from apps.question.models import Question
from apps.user.models import History


class RegisterQuestionAnswer(View):
    """
    解答登録用APIエンドポイント
    """

    def post(self, request: HttpRequest, *args: typing.Any, **kwargs: typing.Any) -> JsonResponse:
        """
        Post メソッド

        Returns:
            JsonResponse: JsonResponse オブジェクト
        """
        self._save_question_answer()
        return JsonResponse({})

    def _save_question_answer(self) -> None:
        """
        解答を保存する。
        """
        pk = self.kwargs['pk']
        user = self.request.user
        if user.is_anonymous:
            return

        selected_choice_ids = self.request.POST.getlist('choice')
        question = Question.objects.get(pk=pk)
        choices = question.choices.filter(pk__in=selected_choice_ids)

        history = History.objects.create(
            user=user,
            question=question,
        )
        history.choices.set(choices)
