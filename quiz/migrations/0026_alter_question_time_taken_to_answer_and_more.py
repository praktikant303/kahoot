# Generated by Django 4.1 on 2022-08-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0025_alter_user_final_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='time_taken_to_answer',
            field=models.FloatField(default=20.0, help_text='Time take to answer'),
        ),
        migrations.AlterField(
            model_name='user',
            name='final_score',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
