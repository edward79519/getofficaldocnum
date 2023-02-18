# Generated by Django 3.1.8 on 2023-01-12 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docnum', '0011_auto_20230103_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalContactLoan',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('add_time', models.DateTimeField(blank=True, editable=False)),
                ('update_time', models.DateTimeField(blank=True, editable=False)),
                ('sn', models.CharField(max_length=12)),
                ('status', models.CharField(choices=[('申請中', '申請中'), ('借出中', '借出中'), ('已歸還', '已歸還'), ('已取消', '已取消')], default='申請中', max_length=8)),
                ('reason', models.CharField(max_length=100)),
                ('out_time', models.DateTimeField(blank=True, null=True)),
                ('in_time', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('contra', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='docnum.contract')),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical contact loan',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ContactLoan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('sn', models.CharField(max_length=12)),
                ('status', models.CharField(choices=[('申請中', '申請中'), ('借出中', '借出中'), ('已歸還', '已歸還'), ('已取消', '已取消')], default='申請中', max_length=8)),
                ('reason', models.CharField(max_length=100)),
                ('out_time', models.DateTimeField(blank=True, null=True)),
                ('in_time', models.DateTimeField(blank=True, null=True)),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('contra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loans', to='docnum.contract')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='docnum_contactloan_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-add_time'],
            },
        ),
    ]