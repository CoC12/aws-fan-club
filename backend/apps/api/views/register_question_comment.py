import typing

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
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
        pk = self.kwargs['pk']
        question = Question.objects.get(pk=pk)
        try:
            self._save_question_comment(question)
        except ValueError:
            return HttpResponseBadRequest('Invalid request')
        return JsonResponse({
            'commentsHtml': render_to_string(
                'components/comment_list.html',
                {
                    'comments': question.get_chat_comments(),
                },
            ),
        })

    def _save_question_comment(self, question: Question) -> None:
        """
        コメントを保存する。

        Args:
            question (Question): Question オブジェクト

        Raises:
            PermissionDenied: 未ログインユーザーによるリクエストの場合
            ValueError: コメントの文字数が 1~1000 の範囲外である場合
        """
        user = self.request.user
        if user.is_anonymous:
            raise PermissionDenied

        comment = self.request.POST.get('comment', '')
        if not (0 < len(comment) <= 1000):
            raise ValueError

        Comment.objects.create(
            question=question,
            comment=comment,
            comment_type=Comment.CommentType.CHAT_COMMENT,
            commented_by=user,
        )
