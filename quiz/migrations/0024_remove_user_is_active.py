# Generated by Django 4.1 on 2022-08-18 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0023_alter_user_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
    ]