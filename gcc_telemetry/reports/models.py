from django.db import models

class Report(models.Model):
    creation_date = models.DateTimeField('date creation')
    test = models.CharField(max_length = 128)
    compiler = models.CharField(max_length = 128)
    options = models.CharField(max_length = 256)
    buildbot = models.CharField(max_length = 128)

class ReportData(models.Model):
    report = models.ForeignKey(Report)
    key = models.CharField(max_length = 128)
    type = models.CharField(max_length = 32)

class PlotData(models.Model):
    report_data = models.ForeignKey(ReportData, null = True)
    name = models.CharField(max_length = 128)
    value = models.FloatField()
