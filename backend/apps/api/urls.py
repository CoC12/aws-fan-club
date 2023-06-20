from django.urls import path

from .views import (
    CreateQuestion,
    CreateQuestionAiComment,
    RegisterQuestionAnswer,
    RegisterQuestionComment,
    RegisterQuestionFeedback,
)

urlpatterns = [
    path('questions/create/', CreateQuestion.as_view(), name='create_question'),
    path('questions/<int:pk>/answers/', RegisterQuestionAnswer.as_view(), name='register_question_answer'),
    path('questions/<int:pk>/comments/', RegisterQuestionComment.as_view(), name='register_question_comment'),
    path('questions/<int:pk>/feedback/', RegisterQuestionFeedback.as_view(), name='register_question_feedback'),
    path(
        'questions/<int:pk>/comments/ai/create/',
        CreateQuestionAiComment.as_view(),
        name='create_question_ai_comment',
    ),
]
