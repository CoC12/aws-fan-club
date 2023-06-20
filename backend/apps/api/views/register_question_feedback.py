import typing

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import View

from apps.question.models import Feedback, Question


class RegisterQuestionFeedback(View):
    """
    フィードバック登録用APIエンドポイント
    """

    def post(self, *args: typing.Any, **kwargs: typing.Any) -> HttpResponse:
        """
        Post メソッド

        Returns:
            HttpResponse: HttpResponse オブジェクト
        """
        pk = self.kwargs['pk']
        question = Question.objects.get(pk=pk)
        try:
            self._save_question_feedback(question)
        except ValueError:
            return HttpResponseBadRequest('Invalid request')
        return JsonResponse(question.get_feedbacks())

    def _save_question_feedback(self, question: Question) -> None:
        """
        フィードバックを保存する。

        Args:
            question (Question): Question オブジェクト

        Raises:
            PermissionDenied: 未ログインユーザーによるリクエストの場合
            ValueError: フィードバックの値が "1", "0" 以外である場合
        """
        user = self.request.user
        if user.is_anonymous:
            raise PermissionDenied

        feedback = self.request.POST.get('feedback')
        if feedback not in ('1', '0'):
            raise ValueError

        Feedback.objects.update_or_create(
            question=question,
            user=user,
            defaults={
                'rating': int(feedback),
            },
        )
