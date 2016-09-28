from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from core.utils import invalidate_caches

from customers.mixins import CustomerMixin, LesserCustomerMixin
from customers.forms import NewCustomerForm, CustomerForm, CustomerScriptForm, CustomerSettingsForm
from customers.forms import MPESAForm, MPESAFormHelper, CustomerRebookingForm, CustomerBirthdayGreetingsForm
from subscriptions.models import Subscription


class NewCustomer(FormView):
    template_name = 'customers/new.html'
    form_class = NewCustomerForm
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super(NewCustomer, self).get_initial()
        initial['email'] = self.request.user.email
        initial['subscription'] = Subscription.objects.filter(default=True).first()
        if 'sub' in self.request.GET and self.request.GET['sub'].isdigit():
            try:
                initial['subscription'] = Subscription.objects.get(pk=int(self.request.GET['sub']))
            except Subscription.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        form.create_new_customer(self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Thank you, welcome to AppointWare'))
        return super(NewCustomer, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if current user is already tied to a customer that has a subscription
        # then redirect them away
        if self.request.user.userprofile.customer and self.request.user.userprofile.customer.has_subscription():
            return redirect('dashboard')
        return super(NewCustomer, self).dispatch(*args, **kwargs)


class EditCustomer(CustomerMixin, FormView):
    template_name = 'customers/edit.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer:edit')

    def get_initial(self):
        initial = super(EditCustomer, self).get_initial()
        initial['name'] = self.customer.name
        initial['email'] = self.customer.email
        initial['phone'] = self.customer.phone
        return initial

    def form_valid(self, form):
        form.save_customer(self.customer)

        # invalidate caches
        invalidate_caches('customeredit', [self.customer.id])
        invalidate_caches('dashboard', [self.customer.id, self.request.user.id])
        invalidate_caches('daycal', [self.customer.id, self.request.user.id])

        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved'))
        return super(EditCustomer, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.customer = self.request.user.userprofile.customer
        return super(EditCustomer, self).dispatch(*args, **kwargs)


class EditCustomerScript(CustomerMixin, FormView):
    template_name = 'customers/script.html'
    form_class = CustomerScriptForm
    success_url = reverse_lazy('customer:script')

    def get_initial(self):
        initial = super(EditCustomerScript, self).get_initial()
        initial['custom_reminder'] = self.customer.custom_reminder
        initial['reminder_sender'] = self.customer.reminder_sender
        initial['reminder_subject'] = self.customer.reminder_subject
        initial['reminder_email'] = self.customer.reminder_email
        initial['reminder_sms'] = self.customer.reminder_sms
        initial['show_confirm_link'] = self.customer.show_confirm_link
        initial['show_cancel_link'] = self.customer.show_cancel_link
        return initial

    def form_valid(self, form):
        form.save_script(self.customer)

        # invalidate caches
        invalidate_caches('customerscript', [self.customer.id])

        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved'))
        return super(EditCustomerScript, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.customer = self.request.user.userprofile.customer
        return super(EditCustomerScript, self).dispatch(*args, **kwargs)


class EditCustomerBirthdayGreetings(CustomerMixin, FormView):
    template_name = 'customers/birthday.html'
    form_class = CustomerBirthdayGreetingsForm
    success_url = reverse_lazy('customer:birthday')

    def get_initial(self):
        initial = super(EditCustomerBirthdayGreetings, self).get_initial()
        initial['birthday_greeting_active'] = self.customer.birthday_greeting_active
        initial['birthday_greeting_sender'] = self.customer.birthday_greeting_sender
        initial['birthday_greeting_subject'] = self.customer.birthday_greeting_subject
        initial['birthday_greeting_email'] = self.customer.birthday_greeting_email
        initial['birthday_greeting_sms'] = self.customer.birthday_greeting_sms
        initial['birthday_greeting_send_email'] = self.customer.birthday_greeting_send_email
        initial['birthday_greeting_send_sms'] = self.customer.birthday_greeting_send_sms
        return initial

    def form_valid(self, form):
        form.save_settings(self.customer)
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved'))
        return super(EditCustomerBirthdayGreetings, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.customer = self.request.user.userprofile.customer
        return super(EditCustomerBirthdayGreetings, self).dispatch(*args, **kwargs)


class EditCustomerRebooking(CustomerMixin, FormView):
    template_name = 'customers/rebooking.html'
    form_class = CustomerRebookingForm
    success_url = reverse_lazy('customer:rebooking')

    def get_initial(self):
        initial = super(EditCustomerRebooking, self).get_initial()
        initial['rebooking_active'] = self.customer.rebooking_active
        initial['rebooking_period'] = self.customer.rebooking_period
        initial['rebooking_period_unit'] = self.customer.rebooking_period_unit
        initial['rebooking_sender'] = self.customer.rebooking_sender
        initial['rebooking_subject'] = self.customer.rebooking_subject
        initial['rebooking_email'] = self.customer.rebooking_email
        initial['rebooking_sms'] = self.customer.rebooking_sms
        initial['rebooking_send_email'] = self.customer.rebooking_send_email
        initial['rebooking_send_sms'] = self.customer.rebooking_send_sms
        return initial

    def form_valid(self, form):
        form.save_settings(self.customer)
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved'))
        return super(EditCustomerRebooking, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.customer = self.request.user.userprofile.customer
        return super(EditCustomerRebooking, self).dispatch(*args, **kwargs)


class EditCustomerSettings(CustomerMixin, FormView):
    template_name = 'customers/settings.html'
    form_class = CustomerSettingsForm
    success_url = reverse_lazy('customer:settings')

    def get_initial(self):
        initial = super(EditCustomerSettings, self).get_initial()
        initial['shown_days'] = self.customer.shown_days
        initial['allow_overlap'] = self.customer.allow_overlap
        initial['send_sms'] = self.customer.send_sms
        initial['send_email'] = self.customer.send_email
        initial['client_display'] = self.customer.client_display
        initial['use_tags'] = self.customer.use_tags
        initial['use_four_day'] = self.customer.use_four_day
        initial['use_no_background_print'] = self.customer.use_no_background_print
        initial['time_slot_height'] = self.customer.time_slot_height
        initial['time_slots_per_hour'] = self.customer.time_slots_per_hour
        return initial

    def form_valid(self, form):
        form.save_settings(self.customer)

        # invalidate caches
        invalidate_caches('customersettings', [self.customer.id])
        invalidate_caches('dashboard', [self.customer.id, self.request.user.id])
        invalidate_caches('daycal', [self.customer.id, self.request.user.id])

        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved'))
        return super(EditCustomerSettings, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.customer = self.request.user.userprofile.customer
        return super(EditCustomerSettings, self).dispatch(*args, **kwargs)


class PlanView(CustomerMixin, FormMixin, DetailView):
    model = Subscription
    template_name = 'customers/subscription_detail.html'

    def get_success_url(self):
        return reverse('customer:subscription')

    def get_form_class(self):
        return MPESAForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save_receipt(self.customer, self.object)
        messages.add_message(
            self.request, messages.SUCCESS, _('Thank you for your payment, we will update your account shortly.'))

        # ivalidate caches
        invalidate_caches('customersubscription', [self.customer.id])
        invalidate_caches('customerpay', [self.customer.id])

        return super(PlanView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PlanView, self).get_context_data(**kwargs)
        form = self.get_form()
        context['form'] = form
        return context

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        self.customer = self.request.user.userprofile.customer
        return super(PlanView, self).dispatch(*args, **kwargs)


class SubscriptionListView(LesserCustomerMixin, ListView):

    model = Subscription
    template_name = 'customers/subscription_list.html'

    def get_context_data(self, **kwargs):
        context = super(SubscriptionListView, self).get_context_data(**kwargs)
        context['form'] = MPESAForm()
        context['MPESAFormHelper'] = MPESAFormHelper
        return context

    def dispatch(self, *args, **kwargs):
        self.customer = self.request.user.userprofile.customer
        return super(SubscriptionListView, self).dispatch(*args, **kwargs)


class PayView(LesserCustomerMixin, FormView):
    template_name = 'customers/pay.html'
    form_class = MPESAForm
    success_url = reverse_lazy('customer:subscription')

    def form_valid(self, form):
        form.save_payment(self.customer)

        # invalidate caches
        invalidate_caches('customersubscription', [self.customer.id])
        invalidate_caches('customerpay', [self.customer.id])

        messages.add_message(
            self.request, messages.SUCCESS, _('Thank you for your payment, we will update your account shortly.'))
        return super(PayView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.customer = self.request.user.userprofile.customer
        return super(PayView, self).dispatch(*args, **kwargs)
