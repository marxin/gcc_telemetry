from django.db import models

class ReportBase(models.Model):
    test = models.CharField(max_length = 128)
    compiler = models.CharField(max_length = 128)
    options = models.CharField(max_length = 256)
    buildbot = models.CharField(max_length = 128)

    def __str__(self):
        return '[test: %s, compiler: %s, options: %s, buildbot: %s]' % (self.test, self.compiler, self.options, self.buildbot)

    def serialize(self):
        return {
            'id': self.id,
            'test': self.test,
            'compiler': self.compiler,
            'options': self.options,
            'buildbot': self.buildbot,
            'name': str(self)
        }

    @staticmethod
    def get(test, compiler, options, buildbot):
        existing = ReportBase.objects.filter(test = test, compiler = compiler, options = options, buildbot = buildbot)
        if len(existing) == 1:
            return existing[0]
        else:
            r = ReportBase(test = test, compiler = compiler, options = options, buildbot = buildbot)
            r.save()
            return r

class Report(models.Model):
    report_base = models.ForeignKey(ReportBase)
    creation_date = models.DateTimeField('date creation')
    revision = models.CharField(max_length = 256)

    def report_data(self):
        return ReportData.objects.filter(report = self)

    def serialize(self):
        return {'report_base': self.report_base.serialize(),
                'revision': self.revision,
                'creation_date': str(self.creation_date),
                'data': [x.serialize() for x in self.report_data()] }

    @staticmethod
    def get_distinct_reports():
        d = {}
        for r in Report.objects.all():
            d[hash(frozenset(r.distinct_object().items()))] = r

        return d.values()

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
