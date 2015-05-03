from django import forms
from django.utils.translation import ugettext as _
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Div, Submit
from dateutil import parser
from schedule.models import Event

from users.models import Client
from doctors.models import Doctor
from venues.models import Venue
from appointments.models import Appointment

from core import labels


class DoctorModelChoiceField(forms.ModelChoiceField):
    pass


class VenueModelChoiceField(forms.ModelChoiceField):
    pass


class AppointmentForm(forms.Form):
    client = forms.IntegerField(
        label=getattr(labels, 'CLIENT', _("Client")),
        required=True,
        widget=forms.HiddenInput
    )
    title = forms.CharField(
        label=_("Title"),
        required=True
    )
    start_date = forms.CharField(
        label=_("Start date"),
        required=True
    )
    start_time = forms.CharField(
        label=_("Start time"),
        required=True
    )
    end_date = forms.CharField(
        label=_("End date"),
        required=False
    )
    end_time = forms.CharField(
        label=_("End time"),
        required=False
    )
    doctor = DoctorModelChoiceField(
        label=getattr(labels, 'DOCTOR', _("Doctor")),
        queryset=Doctor.objects.all(),
    )
    venue = VenueModelChoiceField(
        label=getattr(labels, 'VENUE', _("Venue")),
        queryset=Venue.objects.all(),
    )
    description = forms.CharField(
        label=getattr(labels, 'DESCRIPTION', _("Description")),
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # crispy forms stuff
        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_id = 'id-event-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                _('Create appointment'),
                Div(
                    'title',
                    css_class='form-group'
                ),
                Div(
                    Div(
                        Field('start_date', id="id-appointment-start-date",
                              css_class='start date datetime', autocomplete='off', wrapper_class="datetime"),
                        css_class="col-md-3"
                    ),
                    Div(
                        Field('start_time', id="id-appointment-start-time",
                              css_class='start time datetime', autocomplete='off', wrapper_class="datetime"),
                        css_class="col-md-3"
                    ),
                    Div(
                        Field('end_time', id="id-appointment-end-time",
                              css_class='end time datetime', autocomplete='off', wrapper_class="datetime"),
                        css_class="col-md-3"
                    ),
                    Div(
                        Field('end_date', id="id-appointment-end-date",
                              css_class='end date datetime', autocomplete='off', wrapper_class="datetime"),
                        css_class="col-md-3"
                    ),
                    css_id='id-datetime-pairs',
                    css_class='form-group row form-inline'
                ),
                Div(
                    'doctor',
                    css_class='form-group'
                ),
                Div(
                    'venue',
                    css_class='form-group'
                ),
                Div(
                    'description',
                    Field('client', id="id-create-appointment-client"),
                    css_class='form-group'
                )
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-success')
            )
        )

    def create_event(self, user):
        start = timezone.make_aware(
            parser.parse(
                "%s %s" % (self.cleaned_data['start_date'], self.cleaned_data['start_time']), dayfirst=True),
            timezone.get_current_timezone()
        )
        end = timezone.make_aware(
            parser.parse(
                "%s %s" % (self.cleaned_data['end_date'], self.cleaned_data['end_time']), dayfirst=True),
            timezone.get_current_timezone()
        )
        new_event = Event(
            start=start,
            end=end,
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            creator=user
        )
        new_event.save()
        return new_event

    def create_appointment(self, user):
        event = self.create_event(user)
        new_appointment = Appointment(
            client=Client.objects.get(pk=self.cleaned_data['client']),
            doctor=self.cleaned_data['doctor'],
            venue=self.cleaned_data['venue'],
            event=event,
            creator=user
        )
        new_appointment.save()
        return new_appointment
