from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView

from users.forms import SelectUserForm, AddUserForm

from .forms import AppointmentForm

class AddEventView(TemplateView):
    template_name = 'appointments/add.html'

    def get_context_data(self, **kwargs):
        context = super(AddEventView, self).get_context_data(**kwargs)
        context['SelectUserForm'] = SelectUserForm()
        context['AddUserForm'] = AddUserForm()
        context['AppointmentForm'] = AppointmentForm()
        return context


