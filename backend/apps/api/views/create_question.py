import typing
from subprocess import Popen

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import View

from apps.question.models import Question


class CreateQuestion(View):
    """
    問題生成用APIエンドポイント
    """

    def get(self, *args: typing.Any, **kwargs: typing.Any) -> HttpResponse:
        """
        Get メソッド

        Returns:
            HttpResponse: HttpResponse オブジェクト
        """
        command_args = []

        category_code = self.request.GET.get('category')
        if category_code:
            try:
                category_code_int = int(category_code)
                category = Question.Category(category_code_int)
                command_args.extend([
                    '--category',
                    str(category.value),
                ])
            except Exception:
                return HttpResponseBadRequest()

        Popen([
            'python',
            'manage.py',
            'create_question',
            *command_args,
        ])
        return JsonResponse({})
