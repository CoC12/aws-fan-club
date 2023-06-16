from django.urls import path

from apps.common.views import LoginView

app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
