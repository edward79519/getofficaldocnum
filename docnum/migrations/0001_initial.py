# Generated by Django 3.1.8 on 2021-09-15 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=40)),
                ('shortname', models.CharField(max_length=10)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=10)),
                ('shortname', models.CharField(max_length=10)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OfficalDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=10)),
                ('fullsn', models.CharField(max_length=30)),
                ('pubdate', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='officaldocs', to=settings.AUTH_USER_MODEL)),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='officaldocs', to='docnum.company')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='officaldocs', to='docnum.department')),
            ],
        ),
    ]
