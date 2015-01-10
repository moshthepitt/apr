from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AppointmentForm(forms.Form):
    user = forms.IntegerField(
        label = _("Client"),
        required = True,
        widget = forms.HiddenInput
    )
    title = forms.CharField(
        label = _("Title"),
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
    description = forms.CharField(
        label = _("Description"),
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-event-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.render_hidden_fields = True
