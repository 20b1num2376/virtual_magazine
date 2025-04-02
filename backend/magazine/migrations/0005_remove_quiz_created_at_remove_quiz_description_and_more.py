# Generated by Django 5.0.13 on 2025-03-17 02:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0004_question_quiz_answer_question_quiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='description',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.quiz'),
        ),
    ]
