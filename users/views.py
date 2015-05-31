from django.views.generic import FormView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from django.contrib import messages
from django.http import Http404

from datatableview.views import DatatableView

from customers.mixins import CustomerMixin
from core import labels

from users.models import Client
from users.forms import AddClientForm


class ClientAdd(CustomerMixin, FormView):
    model = Client
    form_class = AddClientForm
    success_url = reverse_lazy('users:list')
    template_name = "users/client_add.html"

    def form_valid(self, form):
        form.create_client(self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved {}'.format(labels.APPOINTMENT)))
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
    form_class = AddClientForm
    template_name = "users/client_edit.html"
    success_url = reverse_lazy('users:list')

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
            'email',
            'phone',
            (_("Actions"), 'id', 'get_actions'),
        ],
        'search_fields': ['first_name', 'last_name', 'email'],
        'unsortable_columns': ['id'],
    }

    def get_actions(self, instance, *args, **kwargs):
        return format_html(
            '<a href="{}">View</a> | <a href="{}">Edit</a> | <a href="{}">Delete</a>', instance.get_absolute_url(), reverse('users:edit', args=[instance.pk]), reverse('users:delete', args=[instance.pk])
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
        return super(ClientDelete, self).delete(request, *args, **kwargs)

    def dispatch(self, *args, **kwargs):
            # if this appointment does not belong to the current customer then raise 404
            if self.request.user.userprofile.customer != self.get_object().customer:
                raise Http404
            return super(ClientDelete, self).dispatch(*args, **kwargs)
