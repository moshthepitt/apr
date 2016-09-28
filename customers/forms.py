# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import Field, FormActions

from customers.models import Customer

from subscriptions.models import Subscription, CustomerSubscription
from invoices.models import Invoice, MPESAReceipt
from venues.utils import new_default_venue


class SubscriptionModelChoiceField(forms.ModelChoiceField):
    pass


class NewCustomerForm(forms.ModelForm):

    """
    Form used by users to sign up for a customer account
    """
    subscription = SubscriptionModelChoiceField(
        label=_("Subscription Plan"),
        queryset=Subscription.objects.exclude(highlighted=False),
    )

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']
        labels = {
            'name': _('Business Name'),
        }

    def create_new_customer(self, user):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        subscription = self.cleaned_data['subscription']
        customer, cu_created = Customer.objects.update_or_create(
            user=user,
            name=name,
            email=email,
            phone=phone
        )
        # subscription
        customer_subscription, sub_created = CustomerSubscription.objects.update_or_create(
            customer=customer, subscription=subscription)
        customer_subscription.start_trial(timezone.now())
        # venue
        new_default_venue(customer)
        # user
        user.userprofile.customer = customer
        user.userprofile.save()
        return customer

    def __init__(self, *args, **kwargs):
        super(NewCustomerForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'id-new-customer-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                _("Set Up Account"),
                'name',
                'email',
                'phone',
                'subscription',
            ),
            FormActions(
                Submit('submit', _('Get Access'), css_class='btn-success')
            )
        )


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']
        labels = {
            'name': _('Business Name'),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'id-customer-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name'),
            Field('email'),
            Field('phone'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )

    def save_customer(self, customer):
        customer.name = self.cleaned_data['name']
        customer.email = self.cleaned_data['email']
        customer.phone = self.cleaned_data['phone']
        customer.save()


class CustomerScriptForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['custom_reminder', 'reminder_sender', 'reminder_subject',
                  'reminder_email', 'reminder_sms', 'show_confirm_link', 'show_cancel_link']

    def __init__(self, *args, **kwargs):
        super(CustomerScriptForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-customer-script-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('custom_reminder'),
            Field('reminder_sender'),
            Field('reminder_subject'),
            Field('reminder_email'),
            Field('reminder_sms'),
            Field('show_confirm_link'),
            Field('show_cancel_link'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )

    def save_script(self, customer):
        customer.custom_reminder = self.cleaned_data['custom_reminder']
        customer.reminder_sender = self.cleaned_data['reminder_sender']
        customer.reminder_subject = self.cleaned_data['reminder_subject']
        customer.reminder_email = self.cleaned_data['reminder_email']
        customer.reminder_sms = self.cleaned_data['reminder_sms']
        customer.show_confirm_link = self.cleaned_data['show_confirm_link']
        customer.show_cancel_link = self.cleaned_data['show_cancel_link']
        customer.save()


class CustomerSettingsForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            'shown_days',
            'allow_overlap',
            'send_sms',
            'send_email',
            'client_display',
            'use_tags',
            'use_four_day',
            'use_no_background_print',
            'time_slot_height',
            'time_slots_per_hour',
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-customer-settings-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('shown_days'),
            Field('client_display'),
            Field('time_slot_height'),
            Field('time_slots_per_hour'),
            Field('allow_overlap'),
            Field('send_sms'),
            Field('send_email'),
            Field('use_tags'),
            Field('use_four_day'),
            Field('use_no_background_print'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )

    def save_settings(self, customer):
        customer.shown_days = self.cleaned_data['shown_days']
        customer.allow_overlap = self.cleaned_data['allow_overlap']
        customer.send_sms = self.cleaned_data['send_sms']
        customer.send_email = self.cleaned_data['send_email']
        customer.client_display = self.cleaned_data['client_display']
        customer.use_tags = self.cleaned_data['use_tags']
        customer.use_four_day = self.cleaned_data['use_four_day']
        customer.use_no_background_print = self.cleaned_data['use_no_background_print']
        customer.time_slot_height = self.cleaned_data['time_slot_height']
        customer.time_slots_per_hour = self.cleaned_data['time_slots_per_hour']
        customer.save()


class CustomerBirthdayGreetingsForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            'birthday_greeting_active',
            'birthday_greeting_sender',
            'birthday_greeting_subject',
            'birthday_greeting_email',
            'birthday_greeting_sms',
            'birthday_greeting_send_email',
            'birthday_greeting_send_sms',
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerBirthdayGreetingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-customer-birthday-greetings-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('birthday_greeting_active'),
            Field('birthday_greeting_sender'),
            Field('birthday_greeting_subject'),
            Field('birthday_greeting_email'),
            Field('birthday_greeting_sms'),
            Field('birthday_greeting_send_email'),
            Field('birthday_greeting_send_sms'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )

    def save_settings(self, customer):
        customer.birthday_greeting_active = self.cleaned_data['birthday_greeting_active']
        customer.birthday_greeting_sender = self.cleaned_data['birthday_greeting_sender']
        customer.birthday_greeting_subject = self.cleaned_data['birthday_greeting_subject']
        customer.birthday_greeting_email = self.cleaned_data['birthday_greeting_email']
        customer.birthday_greeting_sms = self.cleaned_data['birthday_greeting_sms']
        customer.birthday_greeting_send_email = self.cleaned_data['birthday_greeting_send_email']
        customer.birthday_greeting_send_sms = self.cleaned_data['birthday_greeting_send_sms']
        customer.save()


class CustomerRebookingForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            'rebooking_active',
            'rebooking_period',
            'rebooking_period_unit',
            'rebooking_sender',
            'rebooking_subject',
            'rebooking_email',
            'rebooking_sms',
            'rebooking_send_email',
            'rebooking_send_sms',
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerRebookingForm, self).__init__(*args, **kwargs)
        self.fields['rebooking_period'].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'id-customer-birthday-greetings-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('rebooking_active'),
            Field('rebooking_period'),
            Field('rebooking_period_unit'),
            Field('rebooking_sender'),
            Field('rebooking_subject'),
            Field('rebooking_email'),
            Field('rebooking_sms'),
            Field('rebooking_send_email'),
            Field('rebooking_send_sms'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )

    def save_settings(self, customer):
        customer.rebooking_active = self.cleaned_data['rebooking_active']
        customer.rebooking_period = self.cleaned_data['rebooking_period']
        customer.rebooking_period_unit = self.cleaned_data['rebooking_period_unit']
        customer.rebooking_sender = self.cleaned_data['rebooking_sender']
        customer.rebooking_subject = self.cleaned_data['rebooking_subject']
        customer.rebooking_email = self.cleaned_data['rebooking_email']
        customer.rebooking_sms = self.cleaned_data['rebooking_sms']
        customer.rebooking_send_email = self.cleaned_data['rebooking_send_email']
        customer.rebooking_send_sms = self.cleaned_data['rebooking_send_sms']
        customer.save()


class MPESAForm(forms.Form):
    receipt = forms.CharField(label=_("MPESA confirmation code"))

    def save_receipt(self, customer, subscription):
        invoice = Invoice(
            customer=customer,
            date=timezone.now(),
            name=customer.name,
            description=_(
                "Upgrade/downgrade to {subscription}").format(subscription=subscription.name),
            amount=subscription.price,
            method=Invoice.LIPA_NA_MPESA,
            upgrade_to=subscription
        )
        invoice.save()
        receipt, created = MPESAReceipt.objects.get_or_create(
            receipt=self.cleaned_data['receipt'],
            customer=customer,
            invoice=invoice
        )

    def save_payment(self, customer):
        invoice = Invoice(
            customer=customer,
            date=timezone.now(),
            name=customer.name,
            description=_("{subscription} subscription payment").format(
                subscription=customer.customersubscription.subscription),
            amount=customer.customersubscription.subscription.price,
            method=Invoice.LIPA_NA_MPESA,
        )
        invoice.save()
        receipt, created = MPESAReceipt.objects.get_or_create(
            receipt=self.cleaned_data['receipt'],
            customer=customer,
            invoice=invoice
        )

    def __init__(self, *args, **kwargs):
        super(MPESAForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-mpesa-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('receipt'),
            FormActions(
                Submit('submit', _('Submit'), css_class='btn-success')
            )
        )


def MPESAFormHelper():
    """the MPESA form with action to payment page"""
    helper = FormHelper()
    helper.form_id = 'id-mpesa-form'
    helper.form_action = reverse('customer:pay')
    helper.form_method = 'post'
    helper.layout = Layout(
        Field('receipt'),
        FormActions(
            Submit('submit', _('Submit'), css_class='btn-success')
        )
    )

    return helper
