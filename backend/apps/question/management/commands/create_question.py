import logging
import random
import typing

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from apps.question.models import Choice, Question
from services import OpenaiRequestBuilder
from services.json_service import extract_json

logger = logging.getLogger(__name__)


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
    choices: list[ChoiceDict]
    explanation: str


class InvalidResponseFormatException(Exception):
    """
    API レスポンスが不正な場合に送出される例外
    """

    def __init__(self, response: str) -> None:
        """
        __init__ メソッド

        Args:
            response (str): API レスポンス文字列
        """
        self.response = response

    def __str__(self) -> str:
        """
        __str__ メソッド

        Returns:
            str: 文字列表現
        """
        return f'Invalid response format: {self.response}'


class Command(BaseCommand):
    """
    問題作成バッチ
    """

    def add_arguments(self, parser: CommandParser) -> None:
        """
        コマンドの引数を追加する

        Args:
            parser (CommandParser): コマンドパーサ
        """
        parser.add_argument(
            '--category',
            type=int,
            choices=range(1, len(Question.Category.choices) + 1),
            metavar=f'[1-{len(Question.Category.choices)}]',
            help='カテゴリ',
        )

    def handle(self, *args: typing.Any, **options: typing.Any) -> None:
        """
        バッチメイン処理
        """
        category_code = options['category']
        if not category_code:
            category_code = random.choice(Question.Category.values)
        category = Question.Category(category_code)

        try:
            self._execute(category)
        except Exception as e:
            # TODO エラー通知
            raise e

    def _execute(self, category: Question.Category) -> None:
        """
        バッチメイン処理

        Args:
            category (Question.Category): カテゴリ
        """
        logger.info('Starting batch process: create_question')

        request_builder = OpenaiRequestBuilder()
        request_builder.add_system_context(
            '次のJSON形式で出力してください。\n{"question":"string","choices":[{"text":"string","isCorrectAnswer":"bool"}],"explanation":"string"}',  # noqa:E501
        )
        request_builder.add_user_context(
            f'「AWS Certified Cloud Practitioner」の模擬問題を1問、日本語で生成してください。テーマは「{category.label}」とします。',
        )
        response = request_builder.send()

        response_content = response['choices'][0]['message']['content']
        logger.info(f'ChatGPT response: {response_content}')

        try:
            response_json: QuestionDict = extract_json(response_content)
        except Exception as e:
            raise InvalidResponseFormatException(response=response_content) from e

        self._save_question(
            question_data=response_json,
            category=category,
        )
        logger.info('Finished batch process: create_question')

    @transaction.atomic()
    def _save_question(self, question_data: QuestionDict, category: Question.Category) -> None:
        """
        問題を保存する。

        Args:
            question_data (QuestionDataType.QuestionDict): 保存する問題データ
            category (Question.Category): カテゴリ
        """
        created_by = 'ChatGPT'

        question = Question.objects.create(
            text=question_data['question'],
            explanation=question_data['explanation'],
            category=category,
            created_by=created_by,
        )
        choice_list = [
            Choice(
                question=question,
                number=i,
                choice_text=choice['text'],
                is_answer=choice['isCorrectAnswer'],
                created_by=created_by,
            ) for i, choice in enumerate(question_data['choices'], start=1)
        ]
        Choice.objects.bulk_create(choice_list)
