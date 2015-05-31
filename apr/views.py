from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.utils.translation import ugettext as _

from appointments.forms import AppointmentForm, SimpleAppointmentForm, hidden_appointment_form_helper
from users.forms import SelectClientForm, AddClientForm
from users.models import Client
from venues.models import Venue
from subscriptions.models import Subscription
from core.forms import SupportForm
from customers.mixins import CustomerMixin


class DashboardView(CustomerMixin, FormView):
    template_name = 'appointments/calendar.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(customer=self.request.user.userprofile.customer)
        client_form = SelectClientForm()
        client_form.fields['client'].queryset = Client.objects.filter(customer=self.request.user.userprofile.customer)
        context['SelectClientForm'] = client_form
        context['AddClientForm'] = AddClientForm()
        context['AppointmentForm'] = SimpleAppointmentForm()
        context['AppointmentFormHelper'] = hidden_appointment_form_helper
        return context


class PDFView(CustomerMixin, TemplateView):
    template_name = 'appointments/day-pdf.html'

    def get_context_data(self, **kwargs):
        context = super(PDFView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(customer=self.request.user.userprofile.customer)
        return context


class HomeView(TemplateView):
    template_name = 'core/home.html'


class PricingView(ListView):
    template_name = 'core/pricing.html'
    model = Subscription

    def get_queryset(self):
        queryset = Subscription.objects.exclude(highlighted=False)
        return queryset


class CustomerRedirect(RedirectView):
    """
    This view tries to redirect you to the right customer if possible
    """
    permanent = False
    query_string = True
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.userprofile.customer:
            return reverse_lazy('dashboard')
        return super(CustomerRedirect, self).get_redirect_url(*args, **kwargs)


class SupportView(FormView):
    template_name = 'core/support.html'
    form_class = SupportForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully sent email'))
        return super(SupportView, self).form_valid(form)
