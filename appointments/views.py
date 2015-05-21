from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import Http404

from datatableview.views import DatatableView

from users.forms import SelectClientForm, AddClientForm
from appointments.forms import AppointmentForm
from appointments.models import Appointment

from core import labels

from datatableview.utils import FIELD_TYPES
from phonenumber_field.modelfields import PhoneNumberField
FIELD_TYPES['text'].append(PhoneNumberField)


class AppointmentEdit(FormView):
    template_name = 'appointments/edit.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('appointments:appointments')

    def get_success_url(self):
        return reverse_lazy('appointments:appointment', kwargs={'pk': self.object.pk})

    def get_initial(self):
        initial = super(AppointmentEdit, self).get_initial()
        result = initial.copy()
        result.update(self.object.get_form_data())
        return result

    def form_valid(self, form):
        form.edit_appointment(self.object)
        messages.add_message(
            self.request, messages.SUCCESS, 'Successfully saved {}'.format(labels.APPOINTMENT))
        return super(AppointmentEdit, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.object = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        return super(AppointmentEdit, self).dispatch(*args, **kwargs)


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
            object_type = get_object_or_404(
                ContentType, app_label=kwargs['app_label'], model=kwargs['model_name'])
            try:
                this_object = object_type.get_object_for_this_type(pk=kwargs['pk'])
                self.object = this_object
            except:
                raise Http404
        return super(AppointmentListView, self).dispatch(*args, **kwargs)


class AppointmentDatatableView(DatatableView):
    model = Appointment
    template_name = "appointments/appointments_table2.html"
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            (labels.CLIENT_ID, 'client__client_id'),
            (labels.APPOINTMENT, 'event__title'),
            'client',
            (_("Phone"), 'client__phone'),
            'doctor',
            'venue',
            (_("Date"), 'event__start', 'get_date'),
            (_("Actions"), 'id', 'get_actions'),
        ],
        'search_fields': ['client__first_name', 'client__last_name', 'doctor__first_name', 'doctor__last_name', 'venue__name'],
        'unsortable_columns': ['id'],
    }

    def get_date(self, instance, *args, **kwargs):
        return instance.event.start.strftime("%d %b %Y %-I:%M%p")

    def get_actions(self, instance, *args, **kwargs):
        return format_html(
            '<a href="{}">View</a> | <a href="{}">Edit</a> | <a href="{}">Delete</a>', instance.get_absolute_url(), reverse('appointments:appointment_edit', args=[instance.pk]), reverse('appointments:appointment_delete', args=[instance.pk])
        )
