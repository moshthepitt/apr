# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit, HTML, Div
from allauth.utils import generate_unique_username, email_address_exists

from users.models import Client, UserProfile
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
                Submit('submit', _('Submit'), css_class='btn-primary')
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
        fields = ['first_name', 'last_name', 'email', 'phone', 'client_id']

    def create_client(self, user):
        new_client = Client(
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            creator=user,
            customer=user.userprofile.customer
        )
        new_client.save()
        return new_client

    def __init__(self, *args, **kwargs):
        super(AddClientForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['phone'].required = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = False
        self.helper = FormHelper()
        self.helper.form_id = 'id-add-client-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                getattr(labels, 'CREATE_CLIENT', _('Create new client')),
                Field('email', css_class="input-sm"),
                Field('phone', css_class="input-sm"),
                Field('first_name', css_class="input-sm"),
                Field('last_name', css_class="input-sm"),
                Field('client_id', css_class="input-sm"),
            ),
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML("<a class='btn btn-default' href='{% url \"users:list\" %}'>Cancel</a>"),
                css_class="form-group"
            )
        )


def edit_client_helper():
    helper = FormHelper()
    helper.form_id = 'id-edit-client-form'
    helper.form_method = 'post'
    helper.layout = Layout(
        Fieldset(
            getattr(labels, 'EDIT_CLIENT', _('Edit client')),
            'email',
            'phone',
            'first_name',
            'last_name',
            'client_id',
        ),
        ButtonHolder(
            Submit('submit', _('Save'), css_class='btn-success'),
            HTML("<a class='btn btn-default' href='{% url \"users:list\" %}'>Cancel</a>"),
            css_class="form-group"
        )
    )

    return helper


def add_client_form_modal_helper():
    helper = FormHelper()
    helper.form_id = 'id-add-client-form'
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-3'
    helper.field_class = 'col-lg-9'
    helper.layout = Layout(
        Field('email', css_class="input-sm"),
        Field('phone', css_class="input-sm", id="id_phone"),
        Field('first_name', css_class="input-sm"),
        Field('last_name', css_class="input-sm"),
        Field('client_id', css_class="input-sm"),
        Div(
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-sm btn-success'),
                css_class="col-lg-offset-3 col-lg-9"
            ),
            css_class="form-group"
        )
    )

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
        Field('client_id', css_class="input-sm"),
        Div(
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-sm btn-success'),
                css_class="col-lg-offset-3 col-lg-9"
            ),
            css_class="form-group"
        )
    )

    return helper


class AddUserProfileForm(forms.ModelForm):
    role = forms.ChoiceField(label=_("Role"), choices=UserProfile.ROLE_CHOICES, initial=UserProfile.USER)

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
            username=username
        )
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
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('password'),
            Field('role'),
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML("<a class='btn btn-default' href='{% url \"users:staff_list\" %}'>Cancel</a>")
            )
        )


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
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML("<a class='btn btn-default' href='{% url \"users:staff_list\" %}'>Cancel</a>")
            )
        )

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
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-success'),
                HTML("<a class='btn btn-default' href='{% url \"users:staff_list\" %}'>Cancel</a>")
            )
        )
