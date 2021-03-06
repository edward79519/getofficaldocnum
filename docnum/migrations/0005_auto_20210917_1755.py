# Generated by Django 3.1.8 on 2021-09-17 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docnum', '0004_auto_20210917_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officaldoc',
            name='fullsn',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='officaldoc',
            name='sn',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='officaldoc',
            unique_together={('comp', 'dept', 'sn')},
        ),
    ]
