from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Div, Submit
from dateutil import parser
from schedule.models import Event

from appointments.models import Appointment

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
        self.helper.render_hidden_fields = True
        self.helper.form_id = 'id-event-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                _('Create appointment'),
                Div(
                    'title',
                    css_class = 'form-group'
                ),
                Div(
                    Div(
                        Field('start_date', id="id-appointment-start-date", css_class='start date datetime', autocomplete='off', wrapper_class="datetime"),
                        css_class="col-md-3"
                    ),
                    Div(
                        Field('start_time', id="id-appointment-start-time", css_class='start time datetime', autocomplete='off', wrapper_class="datetime"),
                        css_class="col-md-3"
                    ),
                    Div(
                        Field('end_time', id="id-appointment-end-time", css_class='end time datetime', autocomplete='off', wrapper_class="datetime"),
                        css_class="col-md-3"
                    ),
                    Div(
                        Field('end_date', id="id-appointment-end-date", css_class='end date datetime', autocomplete='off', wrapper_class="datetime"),
                        css_class="col-md-3"
                    ),
                    css_id = 'id-datetime-pairs',
                    css_class = 'form-group row form-inline'
                ),
                Div(
                    'description',
                    Field('user', id="id-create-appointment-user"),
                    css_class = 'form-group'
                )
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-success')
            )
        )

    def create_event(self,user):
        start = timezone.make_aware(
            parser.parse("%s %s" %(self.cleaned_data['start_date'],self.cleaned_data['start_time']), dayfirst=True),
            timezone.get_current_timezone()
        )
        end = timezone.make_aware(
            parser.parse("%s %s" %(self.cleaned_data['end_date'],self.cleaned_data['end_time']), dayfirst=True),
            timezone.get_current_timezone()
        )
        new_event = Event(
            start = start,
            end = end,
            title = self.cleaned_data['title'],
            description = self.cleaned_data['description'],
            creator = user
        )
        new_event.save()
        return new_event

    def create_appointment(self,user):
        event = self.create_event(user)
        new_appointment = Appointment(
            user = User.objects.get(pk=self.cleaned_data['user']),
            event = event
        )
        new_appointment.save()
        return new_appointment



