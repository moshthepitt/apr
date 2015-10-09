from django.views.generic import FormView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404

from datatableview.views import DatatableView

from customers.mixins import CustomerMixin
from core import labels
from appointments.models import Appointment

from users.models import Client, UserProfile
from users.forms import EditUserProfileForm, AddUserProfileForm, FullClientForm
from users.forms import EditUserPasswordForm, edit_client_helper

from datatableview.utils import FIELD_TYPES
from phonenumber_field.modelfields import PhoneNumberField
FIELD_TYPES['text'].append(PhoneNumberField)


class ClientAdd(CustomerMixin, FormView):
    model = Client
    form_class = FullClientForm
    success_url = reverse_lazy('users:list')
    template_name = "users/client_add.html"

    def form_valid(self, form):
        form.create_client(self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved client'))
        return super(ClientAdd, self).form_valid(form)


class ClientView(CustomerMixin, DetailView):
    model = Client
    template_name = "users/client_view.html"

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(ClientView, self).dispatch(*args, **kwargs)


class ClientAppointmentsView(CustomerMixin, DatatableView):
    model = Appointment
    template_name = "users/client_appointments.html"
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
        queryset = Appointment.objects.filter(
            customer=self.request.user.userprofile.customer).filter(
            client=self.client)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientAppointmentsView, self).get_context_data(**kwargs)
        context['client'] = self.client
        return context

    def dispatch(self, *args, **kwargs):
        self.client = get_object_or_404(Client, pk=kwargs['pk'])
        return super(ClientAppointmentsView, self).dispatch(*args, **kwargs)


class ClientUpdate(CustomerMixin, UpdateView):
    model = Client
    form_class = FullClientForm
    template_name = "users/client_edit.html"
    success_url = reverse_lazy('users:list')

    def get_context_data(self, **kwargs):
        context = super(ClientUpdate, self).get_context_data(**kwargs)
        context['form_helper'] = edit_client_helper
        return context

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved client'))
        return super(ClientUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(ClientUpdate, self).dispatch(*args, **kwargs)


class ClientDatatableView(CustomerMixin, DatatableView):
    model = Client
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            'first_name',
            'last_name',
            'client_id',
            'email',
            'phone',
            "birth_date",
            (_("Actions"), 'id', 'get_actions'),
        ],
        'search_fields': ['first_name', 'last_name', 'email', 'client_id', 'phone'],
        'unsortable_columns': ['id'],
    }

    def get_actions(self, instance, *args, **kwargs):
        if self.request.user.userprofile.is_admin:
            return format_html(
                '<a href="{}">View</a> | <a href="{}">Appointments</a> | <a href="{}">Edit</a> | <a href="{}">Delete</a>', instance.get_absolute_url(), reverse(
                    'users:client_appointments', args=[instance.pk]), reverse('users:edit', args=[instance.pk]), reverse('users:delete', args=[instance.pk])
            )
        else:
            return format_html(
                '<a href="{}">View</a> | <a href="{}">Appointments</a> | <a href="{}">Edit</a>', instance.get_absolute_url(
                ), reverse('users:client_appointments', args=[instance.pk]), reverse('users:edit', args=[instance.pk])
            )

    def get_queryset(self, **kwargs):
        queryset = Client.objects.filter(customer=self.request.user.userprofile.customer)
        return queryset


class CanceledClientAppointments(CustomerMixin, DatatableView):
    model = Client
    template_name = "users/client_canceled.html"
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            'first_name',
            'last_name',
            'client_id',
            'email',
            'phone',
            (_("Last Appointment"), 'last_appointment', 'get_last_appointment'),
            (_("Actions"), 'id', 'get_actions'),
        ],
        'search_fields': ['first_name', 'last_name', 'email', 'client_id', 'phone'],
        'unsortable_columns': ['id'],
    }

    def get_actions(self, instance, *args, **kwargs):
        return format_html(
            '<a href="{}">Appointments</a>', reverse(
                'users:client_appointments', args=[instance.pk])
        )

    def get_last_appointment(self, instance, *args, **kwargs):
        if instance.last_appointment:
            return timezone.localtime(instance.last_appointment.event.start).strftime("%d %b %Y %-I:%M%p")
        return ""

    def get_queryset(self, **kwargs):
        queryset = Client.objects.filter(customer=self.request.user.userprofile.customer)
        keep = []
        for client in queryset:
            if client.last_appointment and client.last_appointment.status == Appointment.CANCELED:
                keep.append(client.id)
        if keep:
            keep = list(set(keep))
            queryset = queryset.filter(id__in=keep).distinct()
        else:
            queryset = Client.objects.none()
        return queryset


class PendingClientAppointments(CustomerMixin, DatatableView):
    model = Client
    template_name = "users/client_pending.html"
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            'first_name',
            'last_name',
            'client_id',
            'email',
            'phone',
            (_("Last Appointment"), 'last_appointment', 'get_last_appointment'),
            (_("Actions"), 'id', 'get_actions'),
        ],
        'search_fields': ['first_name', 'last_name', 'email', 'client_id', 'phone'],
        'unsortable_columns': ['id'],
    }

    def get_actions(self, instance, *args, **kwargs):
        return format_html(
            '<a href="{}">Appointments</a>', reverse(
                'users:client_appointments', args=[instance.pk])
        )

    def get_last_appointment(self, instance, *args, **kwargs):
        if instance.last_appointment:
            return timezone.localtime(instance.last_appointment.event.start).strftime("%d %b %Y %-I:%M%p")
        return ""

    def get_queryset(self, **kwargs):
        queryset = Client.objects.filter(customer=self.request.user.userprofile.customer)
        keep = []
        for client in queryset:
            if client.last_appointment:
                if client.last_appointment.status != Appointment.SHOWED and client.last_appointment.event.start < timezone.now():
                    keep.append(client.id)
            else:
                keep.append(client.id)
        if keep:
            keep = list(set(keep))
            queryset = queryset.filter(id__in=keep).distinct()
        else:
            queryset = Client.objects.none()
        return queryset


class ClientDelete(CustomerMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('users:list')
    template_name = "users/client_delete.html"

    def delete(self, request, *args, **kwargs):
        """
        Delete all appointments first
        """
        self.get_object().appointment_set.all().delete()
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully deleted {}'.format(labels.APPOINTMENT)))
        return super(ClientDelete, self).delete(request, *args, **kwargs)

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404
        return super(ClientDelete, self).dispatch(*args, **kwargs)


class UserProfileAdd(CustomerMixin, FormView):
    model = UserProfile
    form_class = AddUserProfileForm
    success_url = reverse_lazy('users:staff_list')
    template_name = "users/staff_add.html"

    def form_valid(self, form):
        form.create_userprofile(self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved staff member'))
        return super(UserProfileAdd, self).form_valid(form)


class UserProfileView(CustomerMixin, DetailView):
    model = UserProfile
    template_name = "users/staff_view.html"

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(UserProfileView, self).dispatch(*args, **kwargs)


class UserProfileUpdate(CustomerMixin, UpdateView):
    model = UserProfile
    form_class = EditUserProfileForm
    template_name = "users/staff_edit.html"
    success_url = reverse_lazy('users:staff_list')

    def get_initial(self):
        initial = super(UserProfileUpdate, self).get_initial()
        result = initial.copy()
        result.update(self.object.get_form_data())
        return result

    def form_valid(self, form):
        form.save()
        form.save_user_details(self.get_object())

        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved staff member'))
        return super(UserProfileUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(UserProfileUpdate, self).dispatch(*args, **kwargs)


class UserProfileUpdatePassword(CustomerMixin, UpdateView):
    model = UserProfile
    form_class = EditUserPasswordForm
    template_name = "users/staff_edit.html"
    success_url = reverse_lazy('users:staff_list')

    def form_valid(self, form):
        form.change_password(self.get_object())
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully changed staff member password'))
        return super(UserProfileUpdatePassword, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404

        return super(UserProfileUpdatePassword, self).dispatch(*args, **kwargs)


class UserProfileDatatableView(CustomerMixin, DatatableView):
    model = UserProfile
    template_name = "users/staff_list.html"
    datatable_options = {
        'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            (_("First Name"), 'user__first_name'),
            (_("Last Name"), 'user__last_name'),
            (_("Email"), 'user__email'),
            (_("Role"), 'role', 'get_role'),
            (_("Actions"), 'id', 'get_actions'),
        ],
        'search_fields': ['user__last_name', 'user__first_name', 'user__email'],
        'unsortable_columns': ['id'],
    }

    def get_actions(self, instance, *args, **kwargs):
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Change Password</a>', reverse(
                'users:staff_edit', args=[instance.pk]), reverse('users:staff_edit_password', args=[instance.pk])
        )

    def get_role(self, instance, *args, **kwargs):
        return instance.get_role_display()

    def get_queryset(self, **kwargs):
        queryset = UserProfile.objects.filter(
            customer=self.request.user.userprofile.customer).filter(staff=True)
        return queryset


class UserProfileDelete(CustomerMixin, DeleteView):
    model = UserProfile
    success_url = reverse_lazy('users:staff_list')
    template_name = "users/staff_delete.html"

    def delete(self, request, *args, **kwargs):
        """
        Delete all appointments first
        """
        self.get_object().user.delete()
        self.get_object().appointment_set.all().delete()
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully deleted {}'.format(labels.APPOINTMENT)))
        return super(UserProfileDelete, self).delete(request, *args, **kwargs)

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404
        return super(UserProfileDelete, self).dispatch(*args, **kwargs)
