# Generated by Django 3.1.8 on 2022-12-29 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docnum', '0010_auto_20221223_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='plmsn',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
