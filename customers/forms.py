# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from customers.models import Customer

from venues.utils import new_default_venue
from opening_hours.utils import new_default_opening_hours


class NewCustomerForm(forms.ModelForm):

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
        customer = Customer(
            user=user,
            name=name,
            email=email,
            phone=phone
        )
        customer.save()
        new_default_venue(customer)
        new_default_opening_hours(customer)
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
            ),
            ButtonHolder(
                Submit('submit', 'Get Access', css_class='btn-success')
            )
        )
