from django.contrib import admin

from apps.question.models import Choice, Question


class ChoiceInline(admin.TabularInline[Choice, Question]):
    """
    Choice Admin inline
    """
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin[Question]):
    """
    Question Admin
    """
    inlines = [
        ChoiceInline,
    ]
