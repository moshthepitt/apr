# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit

from users.models import Client
from core import labels


class ClientModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        if obj.first_name:
            return "%s %s" % (obj.first_name, obj.last_name)
        if obj.email:
            return "%s" % obj.email
        return "%s" % obj.username


class SelectClientForm(forms.Form):
    client = ClientModelChoiceField(
        label=getattr(labels, 'CLIENT', _("Client")),
        queryset=Client.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super(SelectClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-select-client-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                getattr(labels, 'SELECT_CLIENT', _('Select client')),
                Field('client', id="id-select-client")
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary')
            )
        )


class AddClientForm(forms.ModelForm):
    """
    Add a new client form
    We have two phone fields
    one will receive the full international number with country code => this is a hidden field
    """

    class Meta:
        model = Client
        fields = ['email', 'phone', 'first_name', 'last_name']

    def create_client(self, user):
        new_client = Client(
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            creator=user
        )
        new_client.save()
        return new_client

    def __init__(self, *args, **kwargs):
        super(AddClientForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'id-add-client-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                getattr(labels, 'CREATE_CLIENT', _('Create new client')),
                'email',
                'phone',
                'first_name',
                'last_name'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary')
            )
        )
