# Generated by Django 3.1.8 on 2021-09-17 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docnum', '0003_officaldoc_addtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officaldoc',
            name='fullsn',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='officaldoc',
            name='sn',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
