from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import Http404

from users.forms import SelectClientForm, AddClientForm
from appointments.forms import AppointmentForm
from appointments.models import Appointment


class AppointmentDelete(DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointments:appointments')


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


class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/appointments.html"

    def get_queryset(self):
        queryset = Appointment.objects.all()
        if self.object:
            if self.object.meta().model_name == "client":
                queryset = queryset.filter(client=self.object)
            elif self.object.meta().model_name == "doctor":
                queryset = queryset.filter(doctor=self.object)
            elif self.object.meta().model_name == "venue":
                queryset = queryset.filter(venue=self.object)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs)
        context['object'] = self.object
        return context

    def dispatch(self, *args, **kwargs):
        allowed_apps = ['users', 'doctors', 'venues']
        self.object = None
        if 'app_label' in kwargs and 'model_name' in kwargs and kwargs['app_label'] in allowed_apps:
            object_type = get_object_or_404(ContentType, app_label=kwargs['app_label'], model=kwargs['model_name'])
            try:
                this_object = object_type.get_object_for_this_type(pk=kwargs['pk'])
                self.object = this_object
            except:
                raise Http404
        return super(AppointmentListView, self).dispatch(*args, **kwargs)
