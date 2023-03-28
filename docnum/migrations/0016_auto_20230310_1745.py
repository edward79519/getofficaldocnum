# Generated by Django 3.1.8 on 2023-03-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docnum', '0015_groupdeptrelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='expiration',
            field=models.CharField(choices=[('未處理', '未處理'), ('待續約', '待續約'), ('待轉約', '待轉約'), ('待增補約', '待增補約'), ('其他', '其他'), ('已終止', '已終止')], default='未處理', max_length=10),
        ),
        migrations.AddField(
            model_name='historicalcontract',
            name='expiration',
            field=models.CharField(choices=[('未處理', '未處理'), ('待續約', '待續約'), ('待轉約', '待轉約'), ('待增補約', '待增補約'), ('其他', '其他'), ('已終止', '已終止')], default='未處理', max_length=10),
        ),
    ]