# Generated by Django 3.1.8 on 2023-05-02 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docnum', '0016_auto_20230310_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='officaldoc',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='receivedoc',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
    ]
