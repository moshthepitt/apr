from django.views.generic import FormView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext as _
from django.utils.html import format_html
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect

from datatableview.views import DatatableView

from customers.mixins import CustomerMixin
from core import labels

from venues.models import Venue
from venues.forms import VenueForm


class VenueAdd(CustomerMixin, FormView):
    model = Venue
    form_class = VenueForm
    success_url = reverse_lazy('venues:list')
    template_name = "venues/venue_add.html"

    def form_valid(self, form):
        form.create_venue(self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved {}'.format(labels.VENUE)))
        return super(VenueAdd, self).form_valid(form)


class VenueView(CustomerMixin, DetailView):
    model = Venue
    template_name = "venues/venue_view.html"

    def dispatch(self, *args, **kwargs):
            # if this appointment does not belong to the current customer then raise 404
            if self.request.user.userprofile.customer != self.get_object().customer:
                raise Http404

            return super(VenueView, self).dispatch(*args, **kwargs)


class VenueUpdate(CustomerMixin, UpdateView):
    model = Venue
    form_class = VenueForm
    template_name = "venues/venue_edit.html"
    success_url = reverse_lazy('venues:list')

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved {}'.format(labels.VENUE)))
        return super(VenueUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
            # if this appointment does not belong to the current customer then raise 404
            if self.request.user.userprofile.customer != self.get_object().customer:
                raise Http404

            return super(VenueUpdate, self).dispatch(*args, **kwargs)


class VenueDatatableView(CustomerMixin, DatatableView):
    model = Venue
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
        return format_html(
            '<a href="{}">View</a> | <a href="{}">Edit</a> | <a href="{}">Delete</a>', instance.get_absolute_url(), reverse('venues:edit', args=[instance.pk]), reverse('venues:delete', args=[instance.pk])
        )

    def get_queryset(self, **kwargs):
        queryset = Venue.objects.filter(customer=self.request.user.userprofile.customer)
        return queryset


class VenueDelete(CustomerMixin, DeleteView):
    model = Venue
    success_url = reverse_lazy('venues:list')
    template_name = "venues/venue_delete.html"

    def delete(self, request, *args, **kwargs):
        """
        Delete all appointments first
        """
        this_appointments = self.get_object().appointment_set.all()
        if this_appointments.count() <= 1:
            messages.add_message(
                self.request, messages.WARNING, _('Cannot delete.  You must have at least one {}'.format(labels.VENUE)))
            return redirect(reverse_lazy('venues:list'))
        else:
            this_appointments.delete()
            messages.add_message(
                self.request, messages.SUCCESS, _('Successfully deleted {}'.format(labels.VENUE)))
            return super(VenueDelete, self).delete(request, *args, **kwargs)

    def dispatch(self, *args, **kwargs):
            # if this appointment does not belong to the current customer then raise 404
            if self.request.user.userprofile.customer != self.get_object().customer:
                raise Http404
            return super(VenueDelete, self).dispatch(*args, **kwargs)


class VenueCalendarView(DetailView):
    model = Venue
    template_name = "venues/venue_calendar.html"
