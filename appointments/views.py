from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import Http404

from datatableview.views import DatatableView

from users.forms import SelectClientForm, AddClientForm, edit_client_form_modal_helper as edit_client_helper
from users.forms import add_client_form_modal_helper as add_client_helper
from appointments.forms import AppointmentForm, EventInfoForm, SimpleAppointmentForm, GenericEventForm
from appointments.forms import hidden_appointment_form_helper, TagForm, edit_generic_event_form_helper
from appointments.models import Appointment, Tag
from appointments.tasks import task_send_cancel_email
from users.models import Client
from venues.models import Venue
from customers.mixins import CustomerMixin, Customer404Mixin

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

    def get_context_data(self, **kwargs):
        context = super(AppointmentEdit, self).get_context_data(**kwargs)
        form = self.get_form()
        form.fields['venue'].queryset = Venue.objects.filter(
            customer=self.request.user.userprofile.customer)
        form.fields['tag'].queryset = Tag.objects.filter(
            customer=self.request.user.userprofile.customer)
        if not self.request.user.userprofile.customer.use_tags:
            del form.fields['tag']
        context['form'] = form
        return context

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


class AppointmentClientConfirm(DetailView):
    model = Appointment
    template_name = 'appointments/client_confirm.html'

    def dispatch(self, *args, **kwargs):
        appointment = self.get_object()
        if appointment.event.start > timezone.now():
            appointment.status = Appointment.CONFIRMED
            appointment.save()
        return super(AppointmentClientConfirm, self).dispatch(*args, **kwargs)


class AppointmentClientCancel(DetailView):
    model = Appointment
    template_name = 'appointments/client_cancel.html'

    def dispatch(self, *args, **kwargs):
        appointment = self.get_object()
        if appointment.event.start > timezone.now() and appointment.status != Appointment.CANCELED:
            appointment.status = Appointment.CANCELED
            appointment.save()
            task_send_cancel_email.delay(appointment.id)
        return super(AppointmentClientCancel, self).dispatch(*args, **kwargs)


class AddEventView(CustomerMixin, TemplateView):
    template_name = 'appointments/add.html'

    def get_context_data(self, **kwargs):
        context = super(AddEventView, self).get_context_data(**kwargs)
        client_form = SelectClientForm()
        client_form.fields['client'].queryset = Client.objects.filter(
            customer=self.request.user.userprofile.customer)
        context['SelectClientForm'] = client_form
        context['AddClientForm'] = AddClientForm()
        appointment_form = AppointmentForm()
        appointment_form.fields['venue'].queryset = Venue.objects.filter(
            customer=self.request.user.userprofile.customer)
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


class AppointmentSnippetView(Customer404Mixin, DetailView):

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
        if event_info_form.fields.get('tag'):
            event_info_form.fields['tag'].queryset = Tag.objects.filter(
                customer=self.request.user.userprofile.customer)
            if self.object.customer.use_tags:
                event_info_form.fields['tag'].initial = self.object.tag
            else:
                del event_info_form.fields['tag']
        context['event_info_form'] = event_info_form
        # generic event
        generic_event_form = GenericEventForm(instance=self.get_object().event)
        generic_event_form.fields['start_datetime'].initial = self.get_object().event.start
        generic_event_form.fields['end_datetime'].initial = self.get_object().event.end
        generic_event_form.fields['venue_id'].initial = self.get_object().venue.id
        generic_event_form.fields['appointment_id'].initial = self.get_object().id
        context['generic_event_form'] = generic_event_form
        context['edit_generic_event_form_helper'] = edit_generic_event_form_helper
        context['object'] = self.object
        return context

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(AppointmentSnippetView, self).dispatch(*args, **kwargs)


class AddAppointmentSnippetView(Customer404Mixin, TemplateView):

    """
    returns modal content when adding new appointment
    """
    template_name = "appointments/snippets/add-appointment.html"

    def get_context_data(self, **kwargs):
        context = super(AddAppointmentSnippetView, self).get_context_data(**kwargs)
        client_form = SelectClientForm()
        client_form.fields['client'].queryset = Client.objects.filter(
            customer=self.request.user.userprofile.customer)
        context['SelectClientForm'] = client_form
        context['AddClientForm'] = AddClientForm()
        context['add_client_helper'] = add_client_helper
        context['GenericEventForm'] = GenericEventForm()
        appointment_form = SimpleAppointmentForm()
        context['AppointmentForm'] = appointment_form
        # set initial data based on GET parameters to facilitate new advert creation
        appointment_form.fields['start_datetime'].initial = self.request.GET.get('start', "")
        appointment_form.fields['end_datetime'].initial = self.request.GET.get('end', "")
        appointment_form.fields['venue_id'].initial = self.request.GET.get('venue_id', "")
        context['AppointmentFormHelper'] = hidden_appointment_form_helper
        return context


class AppointmentDatatableView(CustomerMixin, DatatableView):
    model = Appointment
    template_name = "appointments/appointments_list.html"
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            (labels.APPOINTMENT, 'event__title'),
            'client',
            (_("Phone"), 'client__phone'),
            'venue',
            (_("Date"), 'event__start', 'get_date'),
            'status',
            (_("Actions"), 'id', 'get_actions'),
        ],
        'search_fields': ['client__first_name', 'client__last_name', 'doctor__first_name', 'doctor__last_name', 'venue__name'],
        'unsortable_columns': ['id'],
    }

    def get_date(self, instance, *args, **kwargs):
        return timezone.localtime(instance.event.start).strftime("%d %b %Y %-I:%M%p")

    def get_actions(self, instance, *args, **kwargs):
        return format_html(
            '<a href="{}">View</a> | <a href="{}">Edit</a> | <a href="{}">Delete</a>', instance.get_absolute_url(), reverse(
                'appointments:appointment_edit', args=[instance.pk]), reverse('appointments:appointment_delete', args=[instance.pk])
        )

    def get_queryset(self):
        queryset = Appointment.objects.filter(customer=self.request.user.userprofile.customer).exclude(client=None)
        return queryset


class TagAdd(CustomerMixin, FormView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('appointments:tag_list')
    template_name = "appointments/tag_add.html"

    def form_valid(self, form):
        form.create_tag(self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved tag'))
        return super(TagAdd, self).form_valid(form)


class TagUpdate(CustomerMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "appointments/tag_edit.html"
    success_url = reverse_lazy('appointments:tag_list')

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved tag'))
        return super(TagUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if this tag does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(TagUpdate, self).dispatch(*args, **kwargs)


class TagDatatableView(CustomerMixin, DatatableView):
    model = Tag
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            'name',
            (_("Actions"), 'id', 'get_actions'),
        ],
        'search_fields': ['name'],
        'unsortable_columns': ['id'],
    }

    def get_actions(self, instance, *args, **kwargs):
        if self.request.user.userprofile.is_admin:
            return format_html(
                '<a href="{}">Edit</a> | <a href="{}">Delete</a>', reverse('appointments:tag_edit', args=[instance.pk]), reverse('appointments:tag_delete', args=[instance.pk])
            )
        elif self.request.user.userprofile.is_editor:
            return format_html(
                '<a href="{}">Edit</a>', reverse('appointments:tag_edit', args=[instance.pk])
            )
        else:
            return format_html("")

    def get_queryset(self, **kwargs):
        queryset = Tag.objects.filter(customer=self.request.user.userprofile.customer)
        return queryset


class TagDelete(CustomerMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('appointments:tag_list')
    template_name = "appointments/tag_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully deleted tag'))
        return super(TagDelete, self).delete(request, *args, **kwargs)

    def dispatch(self, *args, **kwargs):
        # if this Tag does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404
        return super(TagDelete, self).dispatch(*args, **kwargs)
