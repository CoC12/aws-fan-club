from django.urls import path

from .views import QuestionList

urlpatterns = [
    path('', QuestionList.as_view(), name='question_list'),
]
