from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from customers.forms import NewCustomerForm


class NewCustomer(FormView):
    template_name = 'customers/new.html'
    form_class = NewCustomerForm
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super(NewCustomer, self).get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        form.create_new_customer(self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Thank you, welcome to AppointWare'))
        return super(NewCustomer, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if current user is already tied to a customer then redirect them away
        if self.request.user.userprofile.customer:
            return redirect('dashboard')

        return super(NewCustomer, self).dispatch(*args, **kwargs)
