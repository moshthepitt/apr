from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.first_name:
            return "%s %s" % (obj.first_name, obj.last_name)
        if obj.email:
            return "%s" % obj.email
        return "%s" % obj.username

class SelectUserForm(forms.Form):
    user = UserModelChoiceField(
        label = _("Client"),
        queryset=User.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super(SelectUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-select-user-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class AddUserForm(forms.Form):
    first_name = forms.CharField(
        label = _("First name"),
        required = True
    )
    last_name = forms.CharField(
        label = _("Last name"),
        required = True
    )
    email = forms.EmailField(
        label = _("Email"),
        required = True
    )

    def create_user(self):
        new_user = User(
            username = self.cleaned_data['email'],
            email = self.cleaned_data['email'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            )
        new_user.save()
        return new_user

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-add-user-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
