from django.urls import path

from .views import CreateQuestion

urlpatterns = [
    path('questions/create/', CreateQuestion.as_view(), name='create_question'),
]
