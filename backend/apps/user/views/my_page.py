import typing

from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest, HttpResponseBase

from apps.common.views import BaseView
from config.sidebar_config import SidebarConfig

from ..forms import UserForm


class MyPage(BaseView):
    """
    マイページ画面
    """
    template_name = 'my_page.html'
    sidebar_items = SidebarConfig.my_page

    def dispatch(self, request: HttpRequest, *args: typing.Any, **kwargs: typing.Any) -> HttpResponseBase:
        """
        dispatchメソッド

        Args:
            request (HttpRequest): HttpRequest オブジェクト

        Returns:
            HttpResponse: HttpResponse オブジェクト
        """
        # TODO: ミドルウェア化
        if request.user.is_anonymous:
            path = request.get_full_path()
            return redirect_to_login(path)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        """
        コンテキストデータを取得する。

        Returns:
            dict[str, typing.Any]: コンテキストデータ
        """
        user = self.request.user
        user_form = UserForm(instance=user)

        context = super().get_context_data(**kwargs)
        context.update({
            'user_setting_card_title': 'アカウント設定',
            'user_setting_fields': user_form.get_user_setting_fields(),
        })
        return context
