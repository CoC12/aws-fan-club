import json
import typing

from django.core.management.base import BaseCommand
from django.db import transaction
from openai import ChatCompletion

from apps.question.models import Choice, Question


class Command(BaseCommand):
    """
    問題作成バッチ
    """

    def handle(self, *args: typing.Any, **options: typing.Any) -> None:
        """
        バッチメイン処理
        """
        context = self._get_context()
        prompt = self._get_prompt()

        response = ChatCompletion.create(  # type: ignore[no-untyped-call]
            model='gpt-3.5-turbo',
            messages=[
                *context,
                *prompt,
            ],
        )
        response_content = response['choices'][0]['message']['content']

        self._save_question(
            question_data=json.loads(response_content),
        )

    def _get_context(self) -> list['OpenAiApiType.MessageDict']:
        """
        Open AI API のリクエストコンテキストを返す。
        """
        # プロンプト文のため、以下の flake8 エラーを無視します。
        #     E501 line too long (435 > 120 characters)
        context: list['OpenAiApiType.MessageDict'] = [
            {
                'role': 'system',
                'content': '次のJSON形式のみを出力してください。\n{"$schema":"http://json-schema.org/draft-07/schema#","title":"Quiz Schema","type":"object","properties":{"question":{"type":"string"},"choices":{"type":"array","items":{"type":"object","properties":{"text":{"type":"string"},"isCorrectAnswer":{"type":"boolean"}},"required":["text","isCorrectAnswer"]}},"explanation":{"type":"string"}},"required":["question","choices","explanation"]}',  # noqa:E501
            },
        ]
        return context

    def _get_prompt(self) -> list['OpenAiApiType.MessageDict']:
        """
        Open AI API のリクエストプロンプトを返す。
        """
        prompt: list['OpenAiApiType.MessageDict'] = [
            {
                'role': 'user',
                'content': '「AWS Certified Cloud Practitioner」の模擬問題を1問生成してください。',
            },
        ]
        return prompt

    @transaction.atomic()
    def _save_question(self, question_data: 'QuestionDataType.QuestionDict') -> None:
        """
        問題を保存する。

        Args:
            question_data (QuestionDataType.QuestionDict): 保存する問題データ
        """
        question = Question.objects.create(
            text=question_data['question'],
            explanation=question_data['explanation'],
        )
        choice_list = [
            Choice(
                question=question,
                number=i,
                choice_text=choice['text'],
                is_answer=choice['isCorrectAnswer'],
            ) for i, choice in enumerate(question_data['choices'], start=1)
        ]
        Choice.objects.bulk_create(choice_list)


class OpenAiApiType:
    """
    Open AI のAPIに関する型
    """
    class UsageDict(typing.TypedDict):
        """
        "usage" の型
        """
        prompt_tokens: int
        completion_tokens: int
        total_tokens: int

    class MessageDict(typing.TypedDict):
        """
        "message" の型
        """
        role: str
        content: str

    class ChoiceDict(typing.TypedDict):
        """
        "choices" の型
        """
        message: 'OpenAiApiType.MessageDict'
        finish_reason: str
        index: int

    class OpenAiApiResponse(typing.TypedDict):
        """
        Open AI API のレスポンスの型
        """
        id: str
        object: str
        created: int
        model: str
        usage: 'OpenAiApiType.UsageDict'
        choices: list['OpenAiApiType.ChoiceDict']


class QuestionDataType:
    """
    問題データに関する型
    """
    class ChoiceDict(typing.TypedDict):
        """
        選択肢データの型
        """
        text: str
        isCorrectAnswer: bool

    class QuestionDict(typing.TypedDict):
        """
        問題データの型
        """
        question: str
        choices: list['QuestionDataType.ChoiceDict']
        explanation: str
