# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

from customers.models import Customer

from subscriptions.models import Subscription, CustomerSubscription
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

    def invalidate_caches(self, customer, user):
        keys = [
            make_template_fragment_key('customeredit', [customer.id, user.id]),
            make_template_fragment_key('dashboard', [customer.id, user.id])
        ]
        for key in keys:
            cache.delete(key)

    def save_customer(self, customer, user):
        customer.name = self.cleaned_data['name']
        customer.email = self.cleaned_data['email']
        customer.phone = self.cleaned_data['phone']
        customer.save()
        self.invalidate_caches(customer, user)
