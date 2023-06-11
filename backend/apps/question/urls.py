from django.urls import path

from .views import QuestionDetail, QuestionList

urlpatterns = [
    path('', QuestionList.as_view(), name='question_list'),
    path('<int:pk>/', QuestionDetail.as_view(), name='question_detail'),
]
