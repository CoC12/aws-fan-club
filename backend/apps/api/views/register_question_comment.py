import typing

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import View

from apps.question.models import Comment, Question


class RegisterQuestionComment(View):
    """
    コメント登録用APIエンドポイント
    """

    def post(self, *args: typing.Any, **kwargs: typing.Any) -> HttpResponse:
        """
        Post メソッド

        Returns:
            JsonResponse: JsonResponse オブジェクト
        """
        try:
            self._save_question_comment()
        except ValueError:
            return HttpResponseBadRequest('Invalid request')
        return JsonResponse({})

    def _save_question_comment(self) -> None:
        """
        コメントを保存する。
        """
        pk = self.kwargs['pk']
        user = self.request.user
        if user.is_anonymous:
            raise PermissionDenied

        comment = self.request.POST.get('comment', '')
        if not (0 < len(comment) <= 1000):
            raise ValueError

        question = Question.objects.get(pk=pk)
        Comment.objects.create(
            question=question,
            comment=comment,
            comment_type=Comment.CommentType.CHAT_COMMENT,
            created_by=user.username,
        )
