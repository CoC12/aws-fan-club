from django.urls import path

from .views import CreateQuestion, CreateQuestionAiComment

urlpatterns = [
    path('questions/create/', CreateQuestion.as_view(), name='create_question'),
    path(
        'questions/<int:pk>/comments/ai/create/',
        CreateQuestionAiComment.as_view(),
        name='create_question_ai_comment',
    ),
]
