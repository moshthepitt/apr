from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from appointments.forms import AppointmentForm
from venues.models import Venue


class DashboardView(FormView):
    template_name = 'appointments/dashboard.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.all()[:3]
        return context

dashboard = DashboardView.as_view()


class HomeView(TemplateView):
    template_name = 'core/home.html'

home = HomeView.as_view()
