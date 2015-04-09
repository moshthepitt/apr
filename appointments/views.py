from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from users.forms import SelectClientForm, AddClientForm
from appointments.forms import AppointmentForm
from appointments.models import Appointment


class AddEventView(TemplateView):
    template_name = 'appointments/add.html'

    def get_context_data(self, **kwargs):
        context = super(AddEventView, self).get_context_data(**kwargs)
        context['SelectClientForm'] = SelectClientForm()
        context['AddClientForm'] = AddClientForm()
        context['AppointmentForm'] = AppointmentForm()
        return context


class AppointmentView(DetailView):
    model = Appointment
    template_name = "appointments/appointment_detail.html"
