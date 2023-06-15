import typing
from enum import Enum

from openai import ChatCompletion


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
    message: MessageDict
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
    usage: UsageDict
    choices: list[ChoiceDict]


class OpenaiRequestBuilder:
    """
    OpenAI へのAPIリクエストを生成する。
    """

    class Model(Enum):
        """
        ChatGPTモデル
        """
        GPT_3_5_TURBO = 'gpt-3.5-turbo'

    def __init__(self) -> None:
        """
        __init__ メソッド
        """
        # 使用するモデル
        self.model = OpenaiRequestBuilder.Model.GPT_3_5_TURBO.value
        # リクエストするコンテキスト
        self.context: list[dict[str, str]] = []

    def set_model(self, model: Model) -> None:
        """
        使用するモデルを指定する。

        Args:
            model (Model): 使用するモデル
        """
        self.model = model.value

    def add_system_context(self, message: str) -> None:
        """
        システムコンテキストを追加する。

        Args:
            message (str): メッセージ
        """
        self._add_context('system', message)

    def add_user_context(self, message: str) -> None:
        """
        ユーザーコンテキストを追加する。

        Args:
            message (str): メッセージ
        """
        self._add_context('user', message)

    def add_assistant_context(self, message: str) -> None:
        """
        アシスタントコンテキストを追加する。

        Args:
            message (str): メッセージ
        """
        self._add_context('assistant', message)

    def send(self) -> OpenAiApiResponse:
        """
        リクエストを送信する。

        Returns:
            OpenAiApiResponse: レスポンス
        """
        response: OpenAiApiResponse = ChatCompletion.create(  # type: ignore[no-untyped-call]
            model=self.model,
            messages=self.context,
        )
        return response

    def _add_context(self, role: str, message: str) -> None:
        """
        コンテキストを追加する。

        Args:
            role (str): 役割
            message (str): メッセージ
        """
        context = {
            'role': role,
            'content': message,
        }
        self.context.append(context)
