# Generated by Django 4.1 on 2022-08-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_question_question_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
