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
from core.generic_views import CoreListView, CoreCreateView
from core.generic_views import CoreUpdateView, CoreDeleteView
from opening_hours.forms import OpeningHourFormSetHelper, OpeningHourFormSet
from appointments.models import Tag

from venues.models import Venue, View
from venues.forms import VenueForm, NoSubmitVenueFormHelper, VenueScriptForm
from venues.forms import ViewForm
from venues.tables import ViewTable


class VenueAdd(CustomerMixin, FormView):
    model = Venue
    form_class = VenueForm
    success_url = reverse_lazy('venues:list')
    template_name = "venues/venue_add.html"

    def form_valid(self, form):
        form.create_venue(self.request.user)
        messages.add_message(
            self.request,
            messages.SUCCESS, _('Successfully saved {}'.format(labels.VENUE)))
        return super(VenueAdd, self).form_valid(form)


class VenueView(CustomerMixin, DetailView):
    model = Venue
    template_name = "venues/venue_view.html"

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then
        # raise 404
        if self.request.user.userprofile.customer !=\
                self.get_object().customer:
            raise Http404

        return super(VenueView, self).dispatch(*args, **kwargs)


class VenueUpdate(CustomerMixin, UpdateView):
    model = Venue
    form_class = VenueForm
    template_name = "venues/venue_edit.html"
    success_url = reverse_lazy('venues:list')

    def get_context_data(self, **kwargs):
        context = super(VenueUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OpeningHourFormSet(self.request.POST,
                                                    instance=self.get_object())
        else:
            context['formset'] = OpeningHourFormSet(instance=self.get_object())
        context['venue_helper'] = NoSubmitVenueFormHelper()
        context['formset_helper'] = OpeningHourFormSetHelper()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            formset.save()
        else:
            return self.form_invalid(form=self.get_form())

        messages.add_message(
            self.request,
            messages.SUCCESS, _('Successfully saved {}'.format(labels.VENUE)))
        return super(VenueUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then
        # raise 404
        if self.request.user.userprofile.customer !=\
                self.get_object().customer:
            raise Http404
        return super(VenueUpdate, self).dispatch(*args, **kwargs)


class VenueScriptUpdate(CustomerMixin, UpdateView):
    model = Venue
    form_class = VenueScriptForm
    template_name = "venues/venue_script.html"
    success_url = reverse_lazy('venues:list')

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS, _('Successfully saved {}'.format(labels.VENUE)))
        return super(VenueScriptUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then
        # raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404
        return super(VenueScriptUpdate, self).dispatch(*args, **kwargs)


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
        if self.request.user.userprofile.is_admin:
            return format_html(
                '<a href="{}">Details</a> | <a href="{}">Calendar</a> | <a href="{}">Edit</a> | <a href="{}">Script</a> | <a href="{}">Delete</a>', instance.get_absolute_url(
                ), reverse('venues:calendar', args=[instance.pk]), reverse('venues:edit', args=[instance.pk]), reverse('venues:script', args=[instance.pk]), reverse('venues:delete', args=[instance.pk])
            )
        elif self.request.user.userprofile.is_editor:
            return format_html(
                '<a href="{}">Details</a> | <a href="{}">Calendar</a> | <a href="{}">Edit</a>', instance.get_absolute_url(
                ), reverse('venues:calendar', args=[instance.pk]), reverse('venues:edit', args=[instance.pk])
            )
        else:
            return format_html(
                '<a href="{}">Calendar</a>', reverse('venues:calendar', args=[instance.pk])
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
        customer_venues = self.get_object().customer.number_of_venues()
        if customer_venues <= 1:
            messages.add_message(
                self.request, messages.WARNING, _('Cannot delete.  You must have at least one {}'.format(labels.VENUE)))
            return redirect(reverse_lazy('venues:list'))
        else:
            this_appointments = self.get_object().appointment_set.all()
            this_appointments.delete()
            messages.add_message(
                self.request, messages.SUCCESS, _('Successfully deleted {}'.format(labels.VENUE)))
            return super(VenueDelete, self).delete(request, *args, **kwargs)

    def dispatch(self, *args, **kwargs):
            # if this appointment does not belong to the current customer then raise 404
        if self.request.user.userprofile.customer != self.get_object().customer:
            raise Http404
        return super(VenueDelete, self).dispatch(*args, **kwargs)


class VenueCalendarView(CustomerMixin, DetailView):
    model = Venue
    template_name = "venues/venue_calendar.html"

    def get_context_data(self, **kwargs):
        context = super(VenueCalendarView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(
            customer=self.request.user.userprofile.customer)
        return context

    def dispatch(self, *args, **kwargs):
        # if this appointment does not belong to the current customer then
        # raise 404
        if self.request.user.userprofile.customer !=\
                self.get_object().customer:
            raise Http404
        return super(VenueCalendarView, self).dispatch(*args, **kwargs)


class ViewListview(CoreListView):
    model = View
    table_class = ViewTable
    search_fields = ['name']

    def get_context_data(self, **kwargs):
        context = super(ViewListview, self).get_context_data(**kwargs)
        context['create_view_url'] = reverse_lazy('venues:views_add')
        context['list_view_url'] = reverse_lazy('venues:views_list')
        return context


class ViewDatatableView(CustomerMixin, DatatableView):
    model = View
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
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>',
            instance.get_edit_url(),
            instance.get_delete_url()
        )

    def get_queryset(self, **kwargs):
        queryset = View.objects.filter(
            customer=self.request.user.userprofile.customer)
        return queryset


class AddView(CoreCreateView):
    model = View
    form_class = ViewForm
    template_name = "venues/view_add.html"


class EditView(CoreUpdateView):
    model = View
    form_class = ViewForm
    template_name = "venues/view_edit.html"


class DeleteView(CoreDeleteView):
    model = View
    success_url = reverse_lazy('venues:views_list')


class DayViewCalendar(CustomerMixin, DetailView):
    """
    Day
    """
    model = View
    template_name = 'venues/venue_calendar_view.html'

    def get_context_data(self, **kwargs):
        context = super(DayViewCalendar, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(
            customer=self.request.user.userprofile.customer)
        return context
