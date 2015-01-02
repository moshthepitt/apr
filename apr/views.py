from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, DeleteView

from appointments.forms import AppointmentForm

class HomeView(FormView):
    template_name = 'appointments/home.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('/')

home = HomeView.as_view()
