import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db import models

from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
from schedule.models import Event

from users.forms import AddClientForm, SelectClientForm, add_client_form_modal_helper, edit_client_form_modal_helper
from appointments.forms import AppointmentForm, SimpleAppointmentForm, EventInfoForm
from appointments.forms import IDForm, GenericEventForm, SimpleGenericEventForm
from appointments.models import Appointment
from users.models import Client
from venues.models import Venue


@csrf_exempt
@json_view
def process_select_client_form(request):
    form = SelectClientForm(request.POST or None)
    form.fields['client'].queryset = Client.objects.filter(
        customer=request.user.userprofile.customer)
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
    form_html = render_crispy_form(form, helper=add_client_form_modal_helper)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_edit_client_form(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = AddClientForm(request.POST or None, instance=client)
    if form.is_valid() and request.user.userprofile.customer == client.customer:
        form.save()
        return {
            'success': True,
            'client_id': client.id
        }
    form_html = render_crispy_form(form, helper=edit_client_form_modal_helper)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_edit_event_form(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventInfoForm(request.POST or None, instance=event)
    appointment = event.appointment_set.first()
    if form.is_valid() and request.user.userprofile.customer == appointment.customer:
        tag = form.cleaned_data.get('tag')
        if tag:
            appointment.tag = tag
            appointment.save()
        form.save()
        return {
            'success': True,
            'event_id': event.id
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_add_event_form(request):
    form = AppointmentForm(request.POST or None)
    form.fields['venue'].queryset = Venue.objects.filter(customer=request.user.userprofile.customer)
    if form.is_valid():
        form.create_appointment(request.user)
        messages.add_message(
            request, messages.SUCCESS, _('Successfully added appointment'))
        return {
            'success': True,
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_generic_event_form(request):
    form = GenericEventForm(request.POST or None)
    if form.is_valid():
        form.create_generic_event(request.user)
        return {
            'success': True,
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_edit_generic_event_form(request):
    form = GenericEventForm(request.POST or None)
    if form.is_valid():
        form.save_edit()
        return {
            'success': True,
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}

# NEW STYLE


def calendar_event_feed(request):
    if request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['start'])), timezone.get_current_timezone())
            to = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['end'])), timezone.get_current_timezone())
            appointments = Appointment.objects.filter(customer=request.user.userprofile.customer).filter(
                models.Q(
                    event__start__gte=fro,
                    event__start__lte=to,
                ) |
                models.Q(
                    event__end__gte=fro,
                    event__end__lte=to,
                ) |
                models.Q(
                    event__start__lt=fro,
                    event__end__gt=to
                )
            )
            data = [x.serialize() for x in appointments]
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


def venue_event_feed(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.is_ajax() and request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['start'])), timezone.get_current_timezone())
            to = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['end'])), timezone.get_current_timezone())
            appointments = Appointment.objects.filter(customer=request.user.userprofile.customer).filter(venue=venue).filter(
                models.Q(
                    event__start__gte=fro,
                    event__start__lte=to,
                ) |
                models.Q(
                    event__end__gte=fro,
                    event__end__lte=to,
                ) |
                models.Q(
                    event__start__lt=fro,
                    event__end__gt=to
                )
            )
            data = [x.serialize(feed='venue') for x in appointments]
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


def printable_event_feed(request):
    if request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['start'])), timezone.get_current_timezone())
            to = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['end'])), timezone.get_current_timezone())
            appointments = Appointment.objects.filter(customer=request.user.userprofile.customer).filter(
                models.Q(
                    event__start__gte=fro,
                    event__start__lte=to,
                ) |
                models.Q(
                    event__end__gte=fro,
                    event__end__lte=to,
                ) |
                models.Q(
                    event__start__lt=fro,
                    event__end__gt=to
                )
            )
            data = [x.serialize(feed='print') for x in appointments]
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


@login_required
def edit_event(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    success = False
    if request.user.userprofile.customer != appointment.customer:
        return False
    if request.is_ajax() and request.method == 'POST':
        if request.POST.get('client'):
            form = SimpleAppointmentForm(request.POST)
            form.fields['venue'].queryset = Venue.objects.filter(
                customer=request.user.userprofile.customer)
            if form.is_valid():
                success = form.save_edit()
        else:
            form = SimpleGenericEventForm(request.POST or None)
            if form.is_valid():
                success = form.save_edit()
    return HttpResponse(json.dumps(success), content_type="application/json")


@login_required
def add_event(request):
    data = {
        "success": False,
        "appointment": {}
    }
    if request.is_ajax() and request.method == 'POST':
        form = SimpleAppointmentForm(request.POST)
        form.fields['venue'].queryset = Venue.objects.filter(
            customer=request.user.userprofile.customer)
        if form.is_valid():
            appointment = form.add_new(request.user)
            data['success'] = True
            data['appointment'] = {
                'id': appointment.pk,
                'title': appointment.display_name,
                'userId': [appointment.venue.pk],
                'start': appointment.event.start.isoformat(),
                'end': appointment.event.end.isoformat(),
                'clientId': appointment.clientId,
                'status': appointment.status,
                'tag': getattr(appointment.tag, 'html_name', ""),
                'body': appointment.event.description
            }
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    success = False
    if request.user.userprofile.customer != appointment.customer:
        return False
    if request.is_ajax() and request.method == 'POST':
        form = IDForm(request.POST)
        if form.is_valid() and form.cleaned_data['id'] == appointment.pk:
            appointment.delete()
            success = True
    return HttpResponse(json.dumps(success), content_type="application/json")


@login_required
def edit_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    success = False
    if request.user.userprofile.customer != appointment.customer:
        return False
    if request.is_ajax() and request.method == 'POST':
        form = IDForm(request.POST)
        if form.is_valid() and form.cleaned_data['id'] == appointment.pk:
            if 'status' in request.POST and request.POST['status'] in Appointment.STATUS_LIST:
                appointment.status = request.POST['status']
                appointment.save()
                success = True
    return HttpResponse(json.dumps(success), content_type="application/json")
