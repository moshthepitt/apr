from django.views.generic import FormView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from django.contrib import messages
from django.http import Http404

from datatableview.views import DatatableView

from customers.mixins import CustomerMixin
from core import labels

from users.models import Client, UserProfile
from users.forms import EditUserProfileForm, AddUserProfileForm, FullClientForm
from users.forms import EditUserPasswordForm, edit_client_helper


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
        'search_fields': ['first_name', 'last_name', 'email', 'client_id'],
        'unsortable_columns': ['id'],
    }

    def get_actions(self, instance, *args, **kwargs):
        if self.request.user.userprofile.is_admin:
            return format_html(
                '<a href="{}">View</a> | <a href="{}">Edit</a> | <a href="{}">Delete</a>', instance.get_absolute_url(), reverse('users:edit', args=[instance.pk]), reverse('users:delete', args=[instance.pk])
            )
        else:
            return format_html(
                '<a href="{}">View</a> | <a href="{}">Edit</a>', instance.get_absolute_url(), reverse('users:edit', args=[instance.pk])
            )

    def get_queryset(self, **kwargs):
        queryset = Client.objects.filter(customer=self.request.user.userprofile.customer)
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
            '<a href="{}">Edit</a> | <a href="{}">Change Password</a>', reverse('users:staff_edit', args=[instance.pk]), reverse('users:staff_edit_password', args=[instance.pk])
        )

    def get_role(self, instance, *args, **kwargs):
        return instance.get_role_display()

    def get_queryset(self, **kwargs):
        queryset = UserProfile.objects.filter(customer=self.request.user.userprofile.customer).filter(staff=True)
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
