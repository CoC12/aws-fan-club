from django import forms

from apps.common.forms import BaseForm

from ..models import User


class UserForm(BaseForm[User]):
    """
    User モデルのフォーム
    """
    class Meta:
        """
        メタクラス
        """
        model = User
        fields = (
            'id',
            'username',
            'email',
        )
        help_texts = {
            'username': '',
        }

    WIDGET_ATTRS = {
        'id': {
            'readonly': True,
        },
        'username': {
            'readonly': True,
        },
        'email': {
            'readonly': True,
        },
    }

    id = forms.IntegerField(
        label='ユーザーID',
    )

    # 「ユーザー設定」エリアに表示するフィールドのフィールド名
    USER_SETTING_FIELDS = [
        'id',
        'username',
        'email',
    ]

    def get_user_setting_fields(self) -> list[forms.BoundField]:
        """
        「ユーザー設定」エリアのフィールドを取得する

        Returns:
            list[forms.BoundField]: 「ユーザー設定」エリアのフィールド
        """
        return self._get_fields_filtered_name(self.USER_SETTING_FIELDS)
