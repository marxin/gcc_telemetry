from django.db import models

class Report(models.Model):
    creation_date = models.DateTimeField('date creation')
    test = models.CharField(max_length = 128)
    compiler = models.CharField(max_length = 128)
    options = models.CharField(max_length = 256)
    buildbot = models.CharField(max_length = 128)
    revision = models.CharField(max_length = 256)

    def report_data(self):
        return ReportData.objects.filter(report = self)

    def serialize(self):
        return { 'test': self.test,
                'compiler': self.compiler,
                'options': self.options,
                'buildbot': self.buildbot,
                'revision': self.revision,
                'creation_date': str(self.creation_date),
                'data': [x.serialize() for x in self.report_data()] }

class ReportData(models.Model):
    report = models.ForeignKey(Report)
    key = models.CharField(max_length = 128)
    type = models.CharField(max_length = 32)

    def plot_data(self):
        return PlotData.objects.filter(report_data = self)

    def serialize(self):
        return { 'key': self.key, 'type': self.type, 'plot': list([x.serialize() for x in self.plot_data()]) }

class PlotData(models.Model):
    report_data = models.ForeignKey(ReportData, null = True)
    name = models.CharField(max_length = 128)
    value = models.FloatField()

    def serialize(self):
        return { 'name': self.name, 'value': self.value }
