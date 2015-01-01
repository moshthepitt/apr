import calendar
import datetime
import json
import time
from dateutil import parser
from django.http import HttpResponse, Http404
from django.utils import timezone

from schedule.models import Event
from schedule.periods import Period

def event_feed(request):
    if request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(parser.parse(request.GET['start']),timezone.get_current_timezone())
            to = timezone.make_aware(parser.parse(request.GET['end']),timezone.get_current_timezone())
            period = Period(Event.objects.all(),fro,to)
            occurences = [{
                            'title':x.title,
                            'className':'event-info',
                            'start':timezone.localtime(x.start).isoformat(),
                            'end':timezone.localtime(x.end).isoformat()
                          }
                          for x in period.get_occurrences()]
        data = occurences
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = {
            "success": 0,
            "error": "Something went wrong"
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
