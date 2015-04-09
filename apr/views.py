from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView

from appointments.forms import AppointmentForm


class HomeView(FormView):
    template_name = 'appointments/home.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('/')

home = HomeView.as_view()
