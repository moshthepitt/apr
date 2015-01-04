from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-user-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
