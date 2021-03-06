﻿import calendar
import datetime
import json
import re
from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse

from NA_DataLayer.common import decorators
from NA_Models.models import LogEvent
from django.db import connection

@decorators.ensure_authorization
@decorators.detail_request_method('GET')
def NA_LogEvent_data(request):
    LogEvent_data = []
    tahun = []
    bulan = []
    hari = []
    ev = (LogEvent.objects.filter(createdby=request.user.username)
                          .values('idapp', 'nameapp', 'createddate'))
    is_filter = request.GET.get('_Search')
    must_filter = False
    if is_filter is not None:
        must_filter = True
    if must_filter:
        filter_log = request.GET['search']
        ev = ev.filter(nameapp__icontains=filter_log)
    #if ev.exists():
    #    event = [i for i in ev.iterator()]  # get log event filter by user
#
    #    for date in ev.dates('createddate', 'year', order='DESC').iterator():
    #        tahun.append(date)
#
    #    for date in ev.dates('createddate', 'month', order='DESC').iterator():
    #        bulan.append(date)
#
    #    for date in ev.dates('createddate', 'day', order='DESC').iterator():
    #        hari.append(date)
#
    #    result = []
    #    for t in tahun:
    #        for b in bulan:
    #            if b.year == t.year:
    #                result.append((str(t.year), b.strftime("%B %Y")))
    #            for h in hari:
    #                if h.year == b.year and h.month == b.month:
    #                    result.append((b.strftime("%B %Y"), h))
    #                for e in event:
    #                    if (e['createddate'].year == h.year and e[
    #                        'createddate'].month == h.month
    #                            and e['createddate'].day == h.day):
    #                        activity = [e['idapp']]
    #                        activity.append('{} at {}'.format(
    #                            e['nameapp'],
    #                            e['createddate'].strftime("%H:%M")
    #                        ))
    #                        result.append(
    #                            (h, activity)
    #                        )
#
    #    parents, children = zip(*result)
    #
    #    root_nodes = {x for x in parents if x not in children}
    #    getUser = str(request.user.username)
    #    for node in root_nodes:
    #        result.append((getUser, node))
    #    result.append(('Log Event', getUser))
    #    
    #    def get_nodes(node):
    #        data = {}
    #        if isinstance(node, list):
    #            data['idapp'] = node[0]
    #            data['text'] = node[1]
    #        else:
    #            data['text'] = node
    #        if data['text'] == str(request.user.username):
    #            data['iconCls'] = 'fa fa-user'
    #        if must_filter:
    #            data['state'] = 'Open'
    #        children = get_children(data['text'])
    #        if children:
    #            data['children'] = [get_nodes(child) for child in children]
    #        return data
#
    #    def get_children(node):
    #        _result = []
    #        for x in result:
    #            if x[0] == node:
    #                _result.append(x[1])
    #        return _result
#
    #    log = get_nodes('Log Event')
    #    LogEvent_data.append(log)
#
    #else:
    #    LogEvent_data = []
#
    #def convert(o):
    #    if isinstance(o, datetime.date):
    #        return '{} {} {}'.format(
    #            o.strftime('%d'),
    #            o.strftime('%B'),
    #            o.strftime('%Y')
    #        )
    #    return o

    result = []
    param_id = request.GET.get('id')
    param_type = request.GET.get('data_type')
    if param_id is None or param_id == "#":
        result.append(
            {
                "id": "root",
                "text": "Log Event",
                "children": True,
                "type": "root"
            }
        )
    elif param_id == "root":
        for date in ev.dates('createddate', 'year', order='DESC').iterator():
            result.append({
                "id": date.year,
                "text": date.year,
                "children": True,
                "type": "year",
                "state": {
                    "opened": False,
                    "disabled": False,
                    "selected": False
                }
            })
    elif param_type == "year":
        months = (ev.filter(createddate__year=param_id).dates(
            'createddate', 'month', order='DESC').iterator()
        )
        for date in months:
            result.append({
                "id": date,
                "text": date.strftime("%B"),
                "children": True,
                "type": "month",
                "state": {
                    "opened": False,
                    "disabled": False,
                    "selected": False
                }
            })
    elif param_type == "month":
        year, month, day = param_id.split('-')
        _, end_date = calendar.monthrange(int(year), int(month))
        dates = ev.filter(createddate__range=[
            param_id, "{}-{}-{}".format(year, month, end_date)
        ]).dates('createddate', 'day', order='DESC').iterator()

        for date in dates:
            result.append({
                "id": date,
                "text": date.strftime("%d %B %Y"),
                "children": True,
                "type": "date",
                "state": {
                    "opened": False,
                    "disabled": False,
                    "selected": False
                }
            })
    elif param_type == "date":
        for e in ev.iterator():
            time_stamp = e['createddate'].strftime("%H:%M")
            result.append({
                "id": e['idapp'],
                "text": "{} {}".format(e['nameapp'],time_stamp),
                "children": False,
                "type": "event",
                "state": {
                    "opened": False,
                    "disabled": False,
                    "selected": False
                }
            })
            
    #print(connection.queries)
   # print(result)
    return JsonResponse(result, safe=False)


@decorators.ensure_authorization
@decorators.ajax_required
@decorators.detail_request_method('GET')
def log_activity_data(request):
    idapp = request.GET.get('idapp')
    log = LogEvent.objects.get(idapp=idapp)
    activity_type = None
    if re.match(r'Created', log.nameapp):
        activity_type = 'created'
    elif re.match(r'Updated', log.nameapp):
        activity_type = 'updated'
    elif re.match(r'Deleted', log.nameapp):
        activity_type = 'deleted'
    result = OrderedDict(
        activity_type=activity_type,
        created_date=log.createddate.strftime('%d %b %Y %H:%M'),
        data={}
    )
    model = ContentType.objects.get(model=log.model).model_class()
    for key in model.HUMAN_DISPLAY.keys():
        value = log.descriptions.get(key)
        if value:
            result['data'].update({
                model.HUMAN_DISPLAY.get(key): value
            })

    return HttpResponse(json.dumps(result), content_type='application/json')
