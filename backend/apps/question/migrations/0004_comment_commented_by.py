# Generated by Django 4.1.5 on 2023-07-06 12:59

from django.apps.registry import Apps
from django.conf import settings
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
import django.db.models.deletion

from apps.user.signals import create_chat_gpt_user


def maintenance_comment_model(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """
    Comment モデルの created_by のユーザーを commented_by に設定する。

    Args:
        apps (Apps): Apps オブジェクト
        schema_editor (BaseDatabaseSchemaEditor): BaseDatabaseSchemaEditor オブジェクト
    """
    create_chat_gpt_user()

    Comment = apps.get_model('question', 'Comment')
    User = apps.get_model('user', 'User')
    for comment in Comment.objects.all():
        commented_user_name = comment.created_by
        user = User.objects.get(username=commented_user_name)
        comment.commented_by = user
        comment.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0003_feedback_feedback_unique_question_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commented_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='コメント者'),
        ),
        migrations.RunPython(maintenance_comment_model),
        migrations.AlterField(
            model_name='comment',
            name='commented_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='コメント者'),
        ),
    ]