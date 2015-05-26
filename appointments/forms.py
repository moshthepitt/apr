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
                "{} {}".format(self.cleaned_data['start_date'], self.cleaned_data['start_time']), dayfirst=True),
            timezone.get_current_timezone()
        )
        end = timezone.make_aware(
            parser.parse(
                "{} {}".format(self.cleaned_data['end_date'], self.cleaned_data['end_time']), dayfirst=True),
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
            creator=user,
            customer=user.userprofile.customer
        )
        new_appointment.save()
        return new_appointment

    def edit_event(self, event):
        event.start = timezone.make_aware(
            parser.parse(
                "%s %s" % (self.cleaned_data['start_date'], self.cleaned_data['start_time']), dayfirst=True),
            timezone.get_current_timezone()
        )
        event.end = timezone.make_aware(
            parser.parse(
                "%s %s" % (self.cleaned_data['end_date'], self.cleaned_data['end_time']), dayfirst=True),
            timezone.get_current_timezone()
        )
        event.title = self.cleaned_data['title']
        event.description = self.cleaned_data['description']
        event.save()

    def edit_appointment(self, appointment):
        self.edit_event(appointment.event)
        appointment.doctor = self.cleaned_data['doctor']
        appointment.venue = self.cleaned_data['venue']
        appointment.save()


class SimpleAppointmentForm(forms.Form):
    id = forms.IntegerField(
        label=_("ID"),
        required=False,
        widget=forms.HiddenInput
    )
    client = forms.IntegerField(
        label=getattr(labels, 'CLIENT', _("Client")),
        required=True,
        widget=forms.HiddenInput
    )
    title = forms.CharField(
        label=_("Title"),
        required=False
    )
    start_datetime = forms.CharField(
        label=_("Start date"),
        required=True
    )
    end_datetime = forms.CharField(
        label=_("End date"),
        required=False
    )
    doctor = DoctorModelChoiceField(
        label=getattr(labels, 'DOCTOR', _("Doctor")),
        queryset=Doctor.objects.all(),
        required=False
    )
    doctor_id = forms.IntegerField(
        label=getattr(labels, 'DOCTOR', _("Doctor")),
        required=False,
        widget=forms.HiddenInput
    )
    venue = VenueModelChoiceField(
        label=getattr(labels, 'VENUE', _("Venue")),
        queryset=Venue.objects.all(),
        required=False
    )
    venue_id = forms.IntegerField(
        label=getattr(labels, 'VENUE', _("Venue")),
        required=False,
        widget=forms.HiddenInput
    )
    description = forms.CharField(
        label=getattr(labels, 'DESCRIPTION', _("Description")),
        required=False,
        widget=forms.Textarea
    )

    def add_new(self, user):
        client = Client.objects.get(pk=self.cleaned_data['client'])
        event = Event(
            start=parser.parse(self.cleaned_data['start_datetime']),
            end=parser.parse(self.cleaned_data['end_datetime']),
            title="{}'s appointment".format(client.get_full_name()),
            creator=user
        )
        event.save()
        appointment = Appointment(
            client=client,
            venue=Venue.objects.get(pk=self.cleaned_data['venue_id']),
            event=event,
            creator=user,
            customer=user.userprofile.customer
        )
        appointment.save()

    def save_edit(self):
        try:
            appointment = Appointment.objects.get(pk=int(self.cleaned_data['id']))
            # appointment
            try:
                client = Client.objects.get(pk=self.cleaned_data['client'])
                appointment.client = client
            except Client.DoesNotExist:
                pass
            if 'doctor' in self.cleaned_data and self.cleaned_data['doctor']:
                appointment.doctor = self.cleaned_data['doctor']
            if 'venue' in self.cleaned_data and self.cleaned_data['venue']:
                appointment.venue = self.cleaned_data['venue']
            appointment.save()
            # event
            if 'title' in self.cleaned_data and self.cleaned_data['title']:
                appointment.event.title = self.cleaned_data['title']
            appointment.event.start = parser.parse(self.cleaned_data['start_datetime'])
            appointment.event.end = parser.parse(self.cleaned_data['end_datetime'])
            if 'description' in self.cleaned_data and self.cleaned_data['description']:
                appointment.event.description = self.cleaned_data['description']
            appointment.event.save()
            return True
        except Appointment.DoesNotExist:
            return False

    def __init__(self, *args, **kwargs):
        super(SimpleAppointmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-simple-add-appointment-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                getattr(labels, 'CREATE_APPOINTMENT', _('Add Appointment')),
                'client',
                'start_datetime',
                'end_datetime',
                'title',
                'doctor',
                'venue',
                'description'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary')
            )
        )


def hidden_appointment_form_helper():
    helper = FormHelper()
    helper.form_id = 'id-hidden-add-appointment-form'
    helper.form_method = 'post'
    helper.layout = Layout(
        Field('client', id="appointment-client-id"),
        Field('start_datetime', id="appointment-start-id"),
        Field('end_datetime', id="appointment-end-id"),
        Field('venue_id', id="appointment-venue-id")
    )
    return helper
