from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from appointments.forms import AppointmentForm
from venues.models import Venue


class HomeView(FormView):
    template_name = 'appointments/home.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('/')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.all()
        return context

home = HomeView.as_view()
