import typing
from subprocess import Popen

from django.http import JsonResponse
from django.views.generic import View


class CreateQuestion(View):
    """
    問題生成用APIエンドポイント
    """

    def get(self, *args: typing.Any, **kwargs: typing.Any) -> JsonResponse:
        """
        Get メソッド

        Returns:
            JsonResponse: JsonResponse オブジェクト
        """
        Popen([
            'python',
            'manage.py',
            'create_question',
        ])
        return JsonResponse({})
