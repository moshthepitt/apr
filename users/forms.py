# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Div
from crispy_forms.bootstrap import Field, FormActions
from allauth.utils import generate_unique_username, email_address_exists

from users.models import Client, UserProfile
from core import labels
from phonenumber_field.formfields import PhoneNumberField
from users.utils import get_client_id


def generate_client_id(client):
    """Generate client id"""
    if not client.client_id:
        client.client_id = get_client_id(
            client=client,
            use_name=True,
        )
        client.save()


class ClientModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.first_name:
            return "%s %s" % (obj.first_name, obj.last_name)
        if obj.email:
            return "%s" % obj.email
        return "%s" % obj.client_id


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
                Field('client', id="id-select-client")),
            FormActions(
                Submit('submit', _('Submit'), css_class='btn-primary')))


class AddClientForm(forms.ModelForm):
    """
    Add a new client form
    """

    class Meta:
        model = Client
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'status',
            'client_id'
        ]

    def create_client(self, user):
        new_client = Client(
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            client_id=self.cleaned_data.get('client_id', None),
            status=self.cleaned_data['status'],
            creator=user,
            customer=user.userprofile.customer)
        new_client.save()
        generate_client_id(client=new_client)
        return new_client

    def __init__(self, *args, **kwargs):
        super(AddClientForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['phone'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['status'].choices = Client.ADD_STATUS_CHOICES
        self.helper = FormHelper()
        self.helper.form_id = 'id-add-client-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                getattr(labels, 'CREATE_CLIENT', _('Create new client')),
                Field('first_name', css_class="input-sm"),
                Field('last_name', css_class="input-sm"),
                Field('phone', css_class="input-sm"),
                Field('email', css_class="input-sm"),
                Field('status', css_class="input-sm"),
                Field('client_id', type="hidden"),
            ),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML(
                    "<a class='btn btn-default' href='{% url \"users:list\" %}'>Cancel</a>"  # noqa
                ),
                css_class="form-group"))


class FullClientForm(forms.ModelForm):
    """
    Add a new client form
    Has all fields
    """
    other_names = forms.CharField(label=_('Other Names'), required=False)
    other_phone = PhoneNumberField(label=_("Other Phone"), required=False)
    first_appointment_date = forms.DateField(
        label=_("First Appointment Date"), required=False)
    address = forms.CharField(
        label=_("Address"),
        widget=forms.Textarea(attrs={
            'rows': 5
        }),
        required=False)
    adult_dependant = forms.ChoiceField(
        label=_("Adult or Dependant"),
        choices=Client.ADULT_DEPENDANT_CHOICES,
        required=False)
    next_of_kin = forms.CharField(
        label=_('Next of Kin Name'), max_length=255, required=False)
    next_of_kin_relationship = forms.CharField(
        label=_('Next of Kin Relationship'), max_length=255, required=False)
    next_of_kin_phone = forms.CharField(
        label=_('Next of Kin Phone Number(s)'), max_length=255, required=False)
    notes = forms.CharField(
        label=_("Notes"),
        widget=forms.Textarea(attrs={
            'rows': 5
        }),
        required=False)

    class Meta:
        model = Client
        fields = [
            'first_name', 'last_name', 'birth_date', 'email', 'phone',
            'client_id', 'status'
        ]

    def create_client(self, user):
        new_client = Client(
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            client_id=self.cleaned_data['client_id'],
            birth_date=self.cleaned_data['birth_date'],
            creator=user,
            customer=user.userprofile.customer)
        new_client.save()
        generate_client_id(client=new_client)
        return new_client

    def clean_client_id(self):
        """Clean client_id"""
        value = self.cleaned_data.get('client_id')
        # pylint: disable=no-member
        if value and Client.objects.exclude(id=self.instance.id).filter(
                client_id=value).exists():
            raise forms.ValidationError(
                _('This client id is already in use.'))
        return value

    def save(self, commit=True):
        """
        Custom save method
        """
        client = super(FullClientForm, self).save()
        data = {
            "other_names": self.cleaned_data.get('other_names'),
            "other_phone": self.cleaned_data.get('other_phone'),
            "first_appointment_date": self.cleaned_data.get(
                'first_appointment_date'),
            "adult_dependant": self.cleaned_data.get('adult_dependant'),
            "address": self.cleaned_data.get('address'),
            "notes": self.cleaned_data.get('notes'),
            "next_of_kin": self.cleaned_data.get('next_of_kin'),
            "next_of_kin_relationship": self.cleaned_data.get(
                'next_of_kin_relationship'),
            "next_of_kin_phone": self.cleaned_data.get('next_of_kin_phone'),
        }
        if data["first_appointment_date"]:
            data["first_appointment_date"] = data[
                "first_appointment_date"].strftime("%x")
        if data["other_phone"]:
            data["other_phone"] = data["other_phone"].as_e164
        client.data = data
        client.save()
        generate_client_id(client=client)
        return client

    def __init__(self, *args, **kwargs):
        super(FullClientForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['phone'].required = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['client_id'].required = False
        self.fields['status'].choices = Client.COMPLETE_STATUS_CHOICES
        self.helper = FormHelper()
        self.helper.form_id = 'id-full-add-client-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                getattr(labels, 'CREATE_CLIENT', _('Create new client')),
                'client_id',
                'first_name',
                'last_name',
                'other_names',
                'email',
                'phone',
                'other_phone',
                Field('birth_date', id="id_birth_date"),
                'adult_dependant',
                Field(
                    'first_appointment_date', id="id_first_appointment_date"),
                'address',
                'next_of_kin',
                'next_of_kin_relationship',
                'next_of_kin_phone',
                'notes',
                'status',
            ),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML(
                    "<a class='btn btn-default' href='{% url \"users:list\" %}'>Cancel</a>"  # noqa
                ),
                css_class="form-group"))


class EditClientFullForm(FullClientForm):
    """Edit client form"""

    def __init__(self, *args, **kwargs):
        super(EditClientFullForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['phone'].required = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['client_id'].required = True


def edit_client_helper():
    helper = FormHelper()
    helper.form_id = 'id-edit-full-client-form'
    helper.form_method = 'post'
    helper.layout = Layout(
        Fieldset(
            getattr(labels, 'EDIT_CLIENT', _('Edit client')),
            'client_id',
            'first_name',
            'last_name',
            'other_names',
            'email',
            'phone',
            'other_phone',
            Field('birth_date', id="id_birth_date"),
            'adult_dependant',
            Field('first_appointment_date', id="id_first_appointment_date"),
            'address',
            'next_of_kin',
            'next_of_kin_relationship',
            'next_of_kin_phone',
            'notes',
            'status',
        ),
        FormActions(
            Submit('submit', _('Save'), css_class='btn-success'),
            HTML(
                "<a class='btn btn-default' href='{% url \"users:list\" %}'>Cancel</a>"  # noqa
            ),
            css_class="form-group"))

    return helper


def add_client_form_modal_helper():
    helper = FormHelper()
    helper.form_id = 'id-add-client-form'
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-3'
    helper.field_class = 'col-lg-9'
    helper.layout = Layout(
        Field('first_name', css_class="input-sm"),
        Field('last_name', css_class="input-sm"),
        Field('phone', css_class="input-sm", id="id_phone"),
        Field('email', css_class="input-sm"),
        Field('status', css_class="input-sm"),
        Field('client_id', type="hidden"),
        Div(FormActions(
            Submit('submit', _('Save'), css_class='btn-sm btn-success'),
            css_class="col-lg-offset-3 col-lg-9"),
            css_class="form-group"))

    return helper


def edit_client_form_modal_helper():
    helper = FormHelper()
    helper.form_id = 'id-edit-client-form'
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-3'
    helper.field_class = 'col-lg-9'
    helper.layout = Layout(
        Field('email', css_class="input-sm"),
        Field('phone', css_class="input-sm", id="id_phone"),
        Field('first_name', css_class="input-sm"),
        Field('last_name', css_class="input-sm"),
        Field('status', css_class="input-sm"),
        Field('client_id', type="hidden"),
        Div(FormActions(
            Submit('submit', _('Save'), css_class='btn-sm btn-success'),
            css_class="col-lg-offset-3 col-lg-9"),
            css_class="form-group"))

    return helper


class AddUserProfileForm(forms.ModelForm):
    role = forms.ChoiceField(
        label=_("Role"),
        choices=UserProfile.ROLE_CHOICES,
        initial=UserProfile.USER)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if email_address_exists(email):
            raise forms.ValidationError(_("This email already exists."))
        return email

    def create_userprofile(self, user):
        username = generate_unique_username([self.cleaned_data['email']])
        password = make_password(self.cleaned_data['password'])
        new_user = User(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=password,
            username=username)
        new_user.save()
        new_user.userprofile.customer = user.userprofile.customer
        new_user.userprofile.role = self.cleaned_data['role']
        new_user.userprofile.staff = True
        new_user.userprofile.save()

        return new_user.userprofile

    def __init__(self, *args, **kwargs):
        super(AddUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'add-userprofile-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name'), Field('last_name'), Field('email'),
            Field('password'), Field('role'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML(
                    "<a class='btn btn-default' href='{% url \"users:staff_list\" %}'>Cancel</a>"  # noqa
                )))


class EditUserPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']

    def __init__(self, *args, **kwargs):
        super(EditUserPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'change-password-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('password'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML(
                    "<a class='btn btn-default' href='{% url \"users:staff_list\" %}'>Cancel</a>"  # noqa
                )))

    def change_password(self, userprofile):
        password = make_password(self.cleaned_data['password'])
        userprofile.user.password = password
        userprofile.user.save()
        return userprofile


class EditUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"), required=False)
    email = forms.EmailField(label=_("Email"))

    class Meta:
        model = UserProfile
        fields = ['role']

    def save_user_details(self, userprofile):
        userprofile.user.email = self.cleaned_data['email']
        userprofile.user.first_name = self.cleaned_data['first_name']
        userprofile.user.last_name = self.cleaned_data['last_name']
        userprofile.user.save()
        return

    def clean_email(self):
        email = self.cleaned_data['email']
        if email_address_exists(email) and email != self.initial['email']:
            raise forms.ValidationError(_("This email already exists."))
        return email

    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'userprofile-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('role'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML(
                    "<a class='btn btn-default' href='{% url \"users:staff_list\" %}'>Cancel</a>"  # noqa
                )))
