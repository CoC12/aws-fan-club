# Generated by Django 4.1.5 on 2023-06-09 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='問題文')),
                ('explanation', models.TextField(blank=True, verbose_name='解説')),
            ],
            options={
                'verbose_name': '問題',
                'verbose_name_plural': '問題一覧',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(verbose_name='選択肢番号')),
                ('choice_text', models.TextField(verbose_name='選択肢文章')),
                ('is_answer', models.BooleanField(default=False, verbose_name='正解か')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='question.question', verbose_name='問題')),
            ],
            options={
                'verbose_name': '選択肢',
                'verbose_name_plural': '選択肢一覧',
                'ordering': ['question', 'number'],
            },
        ),
        migrations.AddConstraint(
            model_name='choice',
            constraint=models.UniqueConstraint(fields=('question', 'number'), name='unique_choice'),
        ),
    ]
