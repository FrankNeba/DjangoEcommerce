# Generated by Django 5.1.1 on 2024-09-07 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
