import typing

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBase,
    HttpResponseRedirect,
)
from django.urls import reverse

from apps.common.dataclass import Button
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

    def post(self, request: HttpRequest, *args: typing.Any, **kwargs: typing.Any) -> HttpResponse:
        """
        POSTメソッド

        Args:
            request (HttpRequest): HttpRequestオブジェクト

        Returns:
            HttpResponse: HttpResponseオブジェクト
        """
        user_form = UserForm(data=request.POST, files=request.FILES, instance=self.request.user)
        is_valid = user_form.is_valid()
        if is_valid:
            user_form.save()
            messages.success(request, '正常に変更されました。')
            success_url = reverse('user:my_page')
            return HttpResponseRedirect(success_url)

        messages.error(request, '正常に変更できませんでした。入力内容を確認してください。')
        context = self.get_context_data(user_form=user_form)
        return self.render_to_response(context)

    def get_context_data(self, user_form: UserForm | None = None, **kwargs: typing.Any) -> dict[str, typing.Any]:
        """
        コンテキストデータを取得する。

        Args:
            user_form (UserForm | None): UserForm オブジェクト

        Returns:
            dict[str, typing.Any]: コンテキストデータ
        """
        if user_form is None:
            user = self.request.user
            user_form = UserForm(instance=user)

        context = super().get_context_data(**kwargs)
        context.update({
            'user_setting_card_title': 'アカウント設定',
            'user_setting_fields': user_form.get_user_setting_fields(),
            'submit_button': Button(
                label='保存',
                submit_form_id='id-mypage__user-setting-form',
            ),
        })
        return context
