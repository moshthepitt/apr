from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AppointmentForm(forms.Form):
    title = forms.CharField(
        label = _("Title"),
        required = True
    )
    name = forms.CharField(
        label = _("Name"),
        required = True
    )
    email = forms.EmailField(
        label = _("Email"),
        required = True
    )
    start_date = forms.CharField(
        label = _("Start date"),
        required = True
    )
    start_time = forms.CharField(
        label = _("Start time"),
        required = True
    )
    end_date = forms.CharField(
        label = _("End date"),
        required = True
    )
    end_time = forms.CharField(
        label = _("End time"),
        required = True
    )
    # description = forms.CharField(
    #     label = _("Description"),
    #     required=False,
    #     widget=forms.Textarea
    # )

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-eventForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
