# Generated by Django 5.1.5 on 2025-02-05 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultrarede', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
