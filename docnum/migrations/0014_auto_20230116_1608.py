# Generated by Django 3.1.8 on 2023-01-16 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docnum', '0013_auto_20230116_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='comp',
            field=models.ForeignKey(limit_choices_to={'valid': True}, on_delete=django.db.models.deletion.PROTECT, related_name='contracts', to='docnum.company'),
        ),
        migrations.AlterField(
            model_name='historicalcontract',
            name='comp',
            field=models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'valid': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='docnum.company'),
        ),
    ]