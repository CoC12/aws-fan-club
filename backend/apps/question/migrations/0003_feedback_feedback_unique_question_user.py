# Generated by Django 4.1.5 on 2023-06-19 14:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('created_by', models.CharField(max_length=256, verbose_name='作成者')),
                ('updated_by', models.CharField(max_length=256, verbose_name='更新者')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='フィードバック')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='question.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'フィードバック',
                'verbose_name_plural': 'フィードバック一覧',
            },
        ),
        migrations.AddConstraint(
            model_name='feedback',
            constraint=models.UniqueConstraint(fields=('question', 'user'), name='unique_question_user'),
        ),
    ]