import typing

from django.http import JsonResponse
from django.views.generic import View

from apps.question.models import Comment, Question
from services import OpenaiRequestBuilder


class CreateQuestionAiComment(View):
    """
    問題に対するAIコメント生成用APIエンドポイント
    """

    def post(self, *args: typing.Any, **kwargs: typing.Any) -> JsonResponse:
        """
        Post メソッド

        Returns:
            JsonResponse: JsonResponse オブジェクト
        """
        pk = self.kwargs['pk']
        question = Question.objects.get(pk=pk)

        request_builder = OpenaiRequestBuilder()
        request_builder.add_user_context(f'AWSにおいて、以下の文章が正しいかどうかを検証してください。\n{question.explanation}')
        response = request_builder.send()

        response_content = response['choices'][0]['message']['content']
        self._save_ai_comment(question, response_content)
        return JsonResponse({'comment': response_content})

    def _save_ai_comment(self, question: Question, comment: str) -> None:
        """
        AIコメントを保存する。

        Args:
            question (Question): 問題モデル
            comment (str): AIコメント
        """
        created_by = 'ChatGPT'

        Comment.objects.create(
            question=question,
            comment=comment,
            comment_type=Comment.CommentType.AI_COMMENT,
            created_by=created_by,
        )
