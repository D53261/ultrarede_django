# Generated by Django 5.1.5 on 2025-02-06 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultrarede', '0004_delete_verifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='checked',
        ),
    ]
