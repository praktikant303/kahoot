# Generated by Django 4.1 on 2022-08-22 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0031_remove_question_technique'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_core',
            field=models.FloatField(default=0, help_text='Score for the answer'),
        ),
    ]