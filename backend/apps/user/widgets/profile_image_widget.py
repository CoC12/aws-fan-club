import typing

from django import forms
from django.db.models.fields.files import ImageFieldFile

from apps.common.dataclass import Avatar


class ProfileImageWidget(forms.ClearableFileInput):
    """
    プロフィール画像ウィジェット
    """
    template_name = 'widgets/profile_image_widget.html'

    def get_context(self, name: str, value: ImageFieldFile, attrs: dict[str, None] | None) -> dict[str, typing.Any]:
        """
        ウィジェットのコンテキストを取得する

        Args:
            name (str): フィールド名
            value (ImageFieldFile): ImageFieldFile オブジェクト
            attrs (dict[str, None] | None): 属性の dict

        Returns:
            dict[str, typing.Any]: ウィジェットのコンテキスト
        """
        context = super().get_context(name, value, attrs)
        context.update({
            'avatar': Avatar(
                absolute_src=value.url,
                size=Avatar.Size.LARGE,
                add_class=[
                    'js-profile-image-widget__preview-image',
                ],
            ),
        })
        return context
