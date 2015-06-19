# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

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
            ButtonHolder(
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
            ButtonHolder(
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
            ButtonHolder(
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
        fields = ['shown_days', 'allow_overlap', 'send_sms', 'send_email']

    def __init__(self, *args, **kwargs):
        super(CustomerSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-customer-settings-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('shown_days'),
            Field('allow_overlap'),
            Field('send_sms'),
            Field('send_email'),
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )

    def save_settings(self, customer):
        customer.shown_days = self.cleaned_data['shown_days']
        customer.allow_overlap = self.cleaned_data['allow_overlap']
        customer.send_sms = self.cleaned_data['send_sms']
        customer.send_email = self.cleaned_data['send_email']
        customer.save()


class MPESAForm(forms.Form):
    receipt = forms.CharField(label=_("MPESA confirmation code"))

    def save_receipt(self, customer, subscription):
        invoice = Invoice(
            customer=customer,
            date=timezone.now(),
            name=customer.name,
            description=_("Upgrade/downgrade {subscription}").format(subscription=subscription.name),
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

    def __init__(self, *args, **kwargs):
        super(MPESAForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-mpesa-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('receipt'),
            ButtonHolder(
                Submit('submit', _('Submit'), css_class='btn-success')
            )
        )
