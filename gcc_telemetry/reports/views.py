import json
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import * 

def from_utc(utcTime,fmt="%Y-%m-%d %H:%M:%S.%f"):
    """
    Convert UTC time string to time.struct_time
    """
    # change datetime.datetime to time, return time.struct_time type
    return datetime.datetime.strptime(utcTime, fmt)

def list(request):
    report_bases = json.dumps([x.serialize() for x in ReportBase.objects.all()], indent = 4)
    return HttpResponse(report_bases, content_type = 'application/json')

def index(request):
    return render(request, 'reports/index.html')

def detail(request, report_base_id):
    base = ReportBase.objects.filter(id = report_base_id)
    reports = Report.objects.filter(report_base = base)

    data_dictionary = {}

    for report in reports:
        for data in report.report_data():
            if not data.key in data_dictionary:
                data_dictionary[data.key] = {}

            v = data_dictionary[data.key]

            for plot in data.plot_data():
                if not plot.name in v:
                    v[plot.name] = []

                p = v[plot.name]
                p.append((report.creation_date.isoformat(), plot.value, report.revision))

    dd = data_dictionary
    transformed = [{ 'key': x, 'plots': [{ 'key': y, 'values': [{'x': z[0], 'y': z[1], 'revision': x[2]} for z in dd[x][y]] } for y in dd[x]] } for x in dd]

    return HttpResponse(json.dumps(transformed, indent = 4), content_type = 'application/json')

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        f = request.FILES['file']
        d = ''
        for chunk in f.chunks():
            d += chunk.decode('utf-8')

        v = json.loads(d)

        report_base = ReportBase.get(v['test'], v['compiler'], v['options'], v['buildbot'])
        report_base.save()

        report = Report(creation_date = from_utc(v['creation_date']), report_base = report_base)
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

