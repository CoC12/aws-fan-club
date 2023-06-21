from django.urls import path

from apps.common.views import LoginView

from .views import MyPage

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('mypage/', MyPage.as_view(), name='my_page'),
]
