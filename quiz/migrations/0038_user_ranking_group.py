# Generated by Django 4.1 on 2022-08-23 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0037_user_quizzes_and_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ranking_group',
            field=models.PositiveSmallIntegerField(blank=True, editable=False, null=True),
        ),
    ]
