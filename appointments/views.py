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

from users.forms import SelectClientForm, AddClientForm, edit_client_helper
from appointments.forms import AppointmentForm, EventInfoForm
from appointments.models import Appointment
from users.models import Client
from venues.models import Venue
from customers.mixins import CustomerMixin

from core import labels

from datatableview.utils import FIELD_TYPES
from phonenumber_field.modelfields import PhoneNumberField
FIELD_TYPES['text'].append(PhoneNumberField)


class AppointmentEdit(CustomerMixin, FormView):
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
            self.request, messages.SUCCESS, _('Successfully saved {}'.format(labels.APPOINTMENT)))
        return super(AppointmentEdit, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.object = get_object_or_404(Appointment, pk=self.kwargs['pk'])
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.object.customer:
            raise Http404

        return super(AppointmentEdit, self).dispatch(*args, **kwargs)


class AppointmentDelete(CustomerMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointments:appointments')

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(AppointmentDelete, self).dispatch(*args, **kwargs)


class AddEventView(CustomerMixin, TemplateView):
    template_name = 'appointments/add.html'

    def get_context_data(self, **kwargs):
        context = super(AddEventView, self).get_context_data(**kwargs)
        client_form = SelectClientForm()
        client_form.fields['client'].queryset = Client.objects.filter(customer=self.request.user.userprofile.customer)
        context['SelectClientForm'] = client_form
        context['AddClientForm'] = AddClientForm()
        appointment_form = AppointmentForm()
        appointment_form.fields['venue'].queryset = Venue.objects.filter(customer=self.request.user.userprofile.customer)
        context['AppointmentForm'] = appointment_form
        return context


class AppointmentView(CustomerMixin, DetailView):
    model = Appointment
    template_name = "appointments/appointment_detail.html"

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(AppointmentView, self).dispatch(*args, **kwargs)


class AppointmentSnippetView(DetailView):
    """
    returns HTML to be used in a modal showing appointment details
    """
    model = Appointment
    template_name = "appointments/snippets/appointment_detail.html"

    def get_context_data(self, **kwargs):
        context = super(AppointmentSnippetView, self).get_context_data(**kwargs)
        edit_client_form = AddClientForm(instance=self.get_object().client)
        context['edit_client_form'] = edit_client_form
        context['edit_client_helper'] = edit_client_helper
        event_info_form = EventInfoForm(instance=self.get_object().event)
        context['event_info_form'] = event_info_form
        context['object'] = self.object
        return context

    def dispatch(self, *args, **kwargs):
        # if current user is not tied to a customer then redirect them away
        if not self.request.user.userprofile.customer:
            raise Http404

        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(AppointmentSnippetView, self).dispatch(*args, **kwargs)


class AppointmentListView(CustomerMixin, ListView):
    model = Appointment
    template_name = "appointments/appointments.html"

    def get_queryset(self):
        queryset = Appointment.objects.filter(customer=self.request.user.userprofile.customer)
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


class AppointmentDatatableView(CustomerMixin, DatatableView):
    model = Appointment
    template_name = "appointments/appointments_table2.html"
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            (labels.APPOINTMENT, 'event__title'),
            'client',
            (_("Phone"), 'client__phone'),
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

    def get_queryset(self):
        queryset = Appointment.objects.filter(customer=self.request.user.userprofile.customer)
        return queryset
