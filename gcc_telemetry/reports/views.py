import json
import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import * 

def from_utc(utcTime,fmt="%Y-%m-%d %H:%M:%S.%f"):
    """
    Convert UTC time string to time.struct_time
    """
    # change datetime.datetime to time, return time.struct_time type
    return datetime.datetime.strptime(utcTime, fmt)

def index(request):
    reports = Report.objects.all()
    return HttpResponse(json.dumps([x.serialize() for x in reports], indent = 4), content_type = 'application/json')

    s = ','.join([x.test + str(x.creation_date) for x in reports])

    return HttpResponse('List of all reports:' + s)

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        f = request.FILES['file']
        d = ''
        for chunk in f.chunks():
            d += chunk.decode('utf-8')

        v = json.loads(d)

        report = Report(creation_date = from_utc(v['creation_date']),
                test = v['test'],
                compiler = v['compiler'],
                options = v['options'],
                buildbot = v['buildbot'])

        report.save()

        for data in v['data']:
            report_data = ReportData(report = report, key = data['name'],
                    type = data['type'])
            report_data.save()

            v = data['values']

            for value in v.keys():
                plot = PlotData(report_data = report_data, name = value,
                        value = float(v[value]))
                plot.save()

        return HttpResponse(str(report))

    return HttpResponse('Nic.')

