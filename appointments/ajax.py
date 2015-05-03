import json
from dateutil import parser
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext as _

from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
from schedule.models import Event
from schedule.periods import Period

from users.forms import AddClientForm, SelectClientForm
from appointments.forms import AppointmentForm
from venues.models import Venue
from doctors.models import Doctor


def event_feed(request):
    if request.is_ajax() and request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                parser.parse(request.GET['start']), timezone.get_current_timezone())
            to = timezone.make_aware(
                parser.parse(request.GET['end']), timezone.get_current_timezone())
            period = Period(Event.objects.exclude(appointment=None), fro, to)
            occurences = [{'id': x.event.appointment_set.first().pk,
                           'title': "%s - %s - %s" % (x.event.appointment_set.first().client, x.event.appointment_set.first().client.client_id, x.title),
                           'className': 'event-info',
                           'start': timezone.localtime(x.start).isoformat(),
                           'end': timezone.localtime(x.end).isoformat(),
                           'resources': [x.event.appointment_set.first().venue.pk]
                           }
                          for x in period.get_occurrences()]
            breaks = [
                {
                    'start': 'T10:00:00',
                    'end': 'T10:30:00',
                    'dow': [1, 2, 3, 4, 5, 6, 7],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                },
                {
                    'start': 'T13:30:00',
                    'end': 'T14:30:00',
                    'dow': [1, 2, 3, 4, 5, 6, 7],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                }
            ]
        data = occurences + breaks
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


def venue_event_feed(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.is_ajax() and request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                parser.parse(request.GET['start']), timezone.get_current_timezone())
            to = timezone.make_aware(
                parser.parse(request.GET['end']), timezone.get_current_timezone())
            period = Period(
                Event.objects.exclude(appointment=None).filter(appointment__venue=venue), fro, to)
            occurences = [{'id': x.event.appointment_set.first().pk,
                           'title': "%s - %s - %s" % (x.event.appointment_set.first().client, x.event.appointment_set.first().client.client_id, x.title),
                           'className': 'event-info',
                           'start': timezone.localtime(x.start).isoformat(),
                           'end': timezone.localtime(x.end).isoformat(),
                           'resources': [x.event.appointment_set.first().venue.pk]
                           }
                          for x in period.get_occurrences()]
            breaks = [
                {
                    'start': 'T10:00:00',
                    'end': 'T10:30:00',
                    'dow': [1, 2, 3, 4, 5, 6, 7],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                },
                {
                    'start': 'T13:30:00',
                    'end': 'T14:30:00',
                    'dow': [1, 2, 3, 4, 5, 6, 7],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                }
            ]
        data = occurences + breaks
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


def doctor_event_feed(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.is_ajax() and request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                parser.parse(request.GET['start']), timezone.get_current_timezone())
            to = timezone.make_aware(
                parser.parse(request.GET['end']), timezone.get_current_timezone())
            period = Period(
                Event.objects.exclude(appointment=None).filter(appointment__doctor=doctor), fro, to)
            occurences = [{'id': x.event.appointment_set.first().pk,
                           'title': "%s - %s - %s" % (x.event.appointment_set.first().client, x.event.appointment_set.first().client.client_id, x.title),
                           'className': 'event-info',
                           'start': timezone.localtime(x.start).isoformat(),
                           'end': timezone.localtime(x.end).isoformat(),
                           'resources': [x.event.appointment_set.first().venue.pk]
                           }
                          for x in period.get_occurrences()]
            breaks = [
                {
                    'start': 'T10:00:00',
                    'end': 'T10:30:00',
                    'dow': [1, 2, 3, 4, 5, 6, 7],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                },
                {
                    'start': 'T13:30:00',
                    'end': 'T14:30:00',
                    'dow': [1, 2, 3, 4, 5, 6, 7],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                }
            ]
        data = occurences + breaks
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


@csrf_exempt
@json_view
def process_select_client_form(request):
    form = SelectClientForm(request.POST or None)
    if form.is_valid():
        return {
            'success': True,
            'client_id': form.cleaned_data['client'].id
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_add_client_form(request):
    form = AddClientForm(request.POST or None)
    if form.is_valid():
        client = form.create_client(request.user)
        return {
            'success': True,
            'client_id': client.id
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_add_event_form(request):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        form.create_appointment(request.user)
        messages.add_message(
            request, messages.SUCCESS, _('Successfully added appointment'))
        return {
            'success': True,
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}
