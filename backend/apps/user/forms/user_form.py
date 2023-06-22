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
            'profile_image',
            'account_id',
            'username',
            'email',
            'bio',
        )
        help_texts = {
            'username': '',
        }

    WIDGET_ATTRS = {
        'account_id': {
            'readonly': True,
        },
        'username': {
            'readonly': True,
        },
        'email': {
            'readonly': True,
        },
    }

    # 「ユーザー設定」エリアに表示するフィールドのフィールド名
    USER_SETTING_FIELDS = [
        'profile_image',
        'account_id',
        'username',
        'email',
        'bio',
    ]

    def get_user_setting_fields(self) -> list[forms.BoundField]:
        """
        「ユーザー設定」エリアのフィールドを取得する

        Returns:
            list[forms.BoundField]: 「ユーザー設定」エリアのフィールド
        """
        return self._get_fields_filtered_name(self.USER_SETTING_FIELDS)
