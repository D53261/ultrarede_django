# Generated by Django 5.1.5 on 2025-02-07 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultrarede', '0006_alter_users_options_alter_users_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='created_at',
        ),
    ]
