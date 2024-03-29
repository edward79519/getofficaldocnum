# Generated by Django 3.1.8 on 2023-01-17 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('docnum', '0014_auto_20230116_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupDeptRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gpdptrlt', to='docnum.department')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gpdptrlt', to='auth.group')),
            ],
            options={
                'unique_together': {('group', 'dept')},
            },
        ),
    ]
