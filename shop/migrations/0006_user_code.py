# Generated by Django 5.1.1 on 2024-09-07 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20240828_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.IntegerField(default=None),
        ),
    ]
