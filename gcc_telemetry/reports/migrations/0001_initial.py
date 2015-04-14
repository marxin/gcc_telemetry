# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(verbose_name='date creation')),
                ('test', models.CharField(max_length=128)),
                ('compiler', models.CharField(max_length=128)),
                ('options', models.CharField(max_length=256)),
                ('buildbot', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ReportData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=32)),
                ('value', models.FloatField()),
                ('report', models.ForeignKey(to='reports.Report')),
            ],
        ),
    ]
