from django.http import JsonResponse
from django.urls import path

urlpatterns = [
    path('sample/', lambda _: JsonResponse({'test': 'test'}), name='sample'),
]
