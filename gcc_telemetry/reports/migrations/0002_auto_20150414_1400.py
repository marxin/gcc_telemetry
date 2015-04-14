# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlotData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='reportdata',
            name='value',
        ),
        migrations.AddField(
            model_name='plotdata',
            name='report_data',
            field=models.ForeignKey(null=True, to='reports.ReportData'),
        ),
    ]
