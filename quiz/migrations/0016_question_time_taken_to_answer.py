# Generated by Django 4.1 on 2022-08-18 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_alter_question_question_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='time_taken_to_answer',
            field=models.FloatField(default=0, help_text='Time take to answer'),
        ),
    ]
