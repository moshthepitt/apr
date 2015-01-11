import json
from dateutil import parser
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
from schedule.models import Event
from schedule.periods import Period

from users.forms import AddUserForm, SelectUserForm
from appointments.forms import AppointmentForm

def event_feed(request):
    if request.is_ajax() and request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(parser.parse(request.GET['start']),timezone.get_current_timezone())
            to = timezone.make_aware(parser.parse(request.GET['end']),timezone.get_current_timezone())
            period = Period(Event.objects.all(),fro,to)
            occurences = [{ 'id': x.pk,
                            'title':x.title,
                            'className':'event-info',
                            'start':timezone.localtime(x.start).isoformat(),
                            'end':timezone.localtime(x.end).isoformat()
                          }
                          for x in period.get_occurrences()]
        data = occurences
        return HttpResponse(json.dumps(data), content_type="application/json")
    #if all fails
    raise Http404

@csrf_exempt
@json_view
def process_select_user_form(request):
    form = SelectUserForm(request.POST or None)
    if form.is_valid():
        return {
            'success': True,
            'user_id': form.cleaned_data['user'].id
            }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}

@csrf_exempt
@json_view
def process_add_user_form(request):
    form = AddUserForm(request.POST or None)
    if form.is_valid():
        user = form.create_user()
        return {
            'success': True,
            'user_id': user.id
            }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}

@csrf_exempt
@json_view
def process_add_event_form(request):
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        appointment = form.create_appointment(request.user)
        return {
            'success': True,
            }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}
