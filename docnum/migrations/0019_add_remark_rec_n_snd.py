# Generated by Django 3.1.8 on 2023-08-21 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docnum', '0018_auto_20230502_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='officaldoc',
            name='remark',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='receivedoc',
            name='remark',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
