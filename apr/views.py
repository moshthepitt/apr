from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, RedirectView
from django.shortcuts import redirect

from wkhtmltopdf.views import PDFTemplateView

from appointments.forms import AppointmentForm
from venues.models import Venue


class DashboardView(FormView):
    template_name = 'appointments/calendar.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(customer=self.request.user.userprofile.customer)
        return context

    def dispatch(self, *args, **kwargs):
        # if current user is not tied to a customer then redirect them away
        if not self.request.user.userprofile.customer:
            return redirect('customer_redirect')
        return super(DashboardView, self).dispatch(*args, **kwargs)


class PDFView(TemplateView):
    template_name = 'appointments/day-pdf.html'

    def get_context_data(self, **kwargs):
        context = super(PDFView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(customer=self.request.user.userprofile.customer)
        return context

    def dispatch(self, *args, **kwargs):
        # if current user is not tied to a customer then redirect them away
        if not self.request.user.userprofile.customer:
            return redirect('customer_redirect')
        return super(PDFView, self).dispatch(*args, **kwargs)


class HomeView(TemplateView):
    template_name = 'core/home.html'


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
