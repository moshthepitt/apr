from re import match
from django import forms
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.forms import ValidationError
from django.utils.encoding import smart_unicode

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit
from crispy_forms.bootstrap import Field, FormActions
from dateutil import parser
from schedule.models import Event

from users.models import Client
from doctors.models import Doctor
from venues.models import Venue
from appointments.models import Appointment, Tag

from core import labels


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
    venue = forms.ModelChoiceField(
        label=getattr(labels, 'VENUE', _("Venue")),
        queryset=Venue.objects.all(),
    )
    tag = forms.ModelChoiceField(
        label=_("Tag"),
        queryset=Tag.objects.all(),
        required=False
    )
    description = forms.CharField(
        label=getattr(labels, 'DESCRIPTION', _("Description")),
        required=False,
        widget=forms.Textarea
    )
    status = forms.ChoiceField(
        label=_("Status"),
        required=True,
        choices=Appointment.STATUS_CHOICES
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
                _('Appointment Details'),
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
                    Field('venue', id="id-venue"),
                    css_class='form-group'
                ),
                Div(
                    Field('tag', id="id-tag"),
                    css_class='form-group'
                ),
                Div(
                    'description',
                    Field('client', id="id-create-appointment-client"),
                    css_class='form-group'
                ),
                Div(
                    Field('status'),
                    css_class='form-group'
                ),
            ),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
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
        appointment.venue = self.cleaned_data['venue']
        appointment.tag = self.cleaned_data['tag']
        appointment.status = self.cleaned_data['status']
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
    doctor = forms.ModelChoiceField(
        label=getattr(labels, 'DOCTOR', _("Doctor")),
        queryset=Doctor.objects.all(),
        required=False
    )
    doctor_id = forms.IntegerField(
        label=getattr(labels, 'DOCTOR', _("Doctor")),
        required=False,
        widget=forms.HiddenInput
    )
    venue = forms.ModelChoiceField(
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
        try:
            client = Client.objects.get(pk=self.cleaned_data['client'])

            if client.phone:
                event_title = "{name} {phone} {id}".format(
                    name=client.get_full_name(), phone=client.phone, id=client.client_id)
            else:
                event_title = "{name} {id}".format(name=client.get_full_name(), id=client.client_id)

            event = Event(
                start=parser.parse(self.cleaned_data['start_datetime']),
                end=parser.parse(self.cleaned_data['end_datetime']),
                title=event_title,
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
            return appointment
        except Client.DoesNotExist:
            return False

    def save_edit(self):
        try:
            appointment = Appointment.objects.get(pk=int(self.cleaned_data['id']))
            # appointment
            if self.cleaned_data.get('client'):
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
            FormActions(
                Submit('submit', _('Save'), css_class='btn-primary')
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


class EventInfoForm(forms.ModelForm):

    """
    Form used to edit event info. i.e title and description
    """
    tag = forms.ModelChoiceField(
        label=_("Tag"),
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Event
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super(EventInfoForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['description'].required = False
        self.helper = FormHelper()
        self.helper.form_id = 'id-event-info-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title', css_class="input-sm"),
            Field('description', css_class="input-sm"),
            Field('tag', id="id-tag", css_class="input-sm"),
            Div(
                FormActions(
                    Submit('submit', _('Save'), css_class='btn-sm btn-success'),
                    css_class="col-lg-offset-2 col-lg-10"
                ),
                css_class="form-group"
            )
        )


class GenericEventForm(forms.ModelForm):

    """
    Form used to deal with events that are not appointments
    """
    start_datetime = forms.CharField(
        label=_("Start date"),
        required=True,
        widget=forms.HiddenInput
    )
    end_datetime = forms.CharField(
        label=_("End date"),
        required=False,
        widget=forms.HiddenInput
    )
    venue_id = forms.IntegerField(
        label=getattr(labels, 'VENUE', _("Venue")),
        required=False,
        widget=forms.HiddenInput
    )
    appointment_id = forms.IntegerField(
        label=_("Appointment"),
        required=False,
        widget=forms.HiddenInput
    )

    class Meta:
        model = Event
        fields = ['title', 'description']

    def create_event(self, user):
        start = parser.parse(self.cleaned_data['start_datetime'])
        end = parser.parse(self.cleaned_data['end_datetime'])
        new_event = Event(
            start=start,
            end=end,
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            creator=user
        )
        new_event.save()
        return new_event

    def create_generic_event(self, user):
        event = self.create_event(user)
        new_appointment = Appointment(
            client=None,
            venue=Venue.objects.get(pk=self.cleaned_data['venue_id']),
            event=event,
            creator=user,
            customer=user.userprofile.customer
        )
        new_appointment.save()
        return new_appointment

    def save_edit(self):
        try:
            appointment = Appointment.objects.get(pk=int(self.cleaned_data['appointment_id']))
            if 'venue' in self.cleaned_data and self.cleaned_data['venue']:
                appointment.venue = self.cleaned_data['venue']
            appointment.save()
            # event
            if 'title' in self.cleaned_data and self.cleaned_data['title']:
                appointment.event.title = self.cleaned_data['title']
            if 'description' in self.cleaned_data and self.cleaned_data['description']:
                appointment.event.description = self.cleaned_data['description']
            else:
                appointment.event.description = ""
            appointment.event.start = parser.parse(self.cleaned_data['start_datetime'])
            appointment.event.end = parser.parse(self.cleaned_data['end_datetime'])
            appointment.event.save()
            return True
        except Appointment.DoesNotExist:
            return False

    def __init__(self, *args, **kwargs):
        super(GenericEventForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['description'].required = False
        self.helper = FormHelper()
        self.helper.form_id = 'id-generic-event-info-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title', css_class="input-sm"),
            Field('description', css_class="input-sm"),
            Field(
                'start_datetime', css_class="input-sm",
                id="generic-start"
            ),
            Field(
                'end_datetime', css_class="input-sm",
                id="generic-end"
            ),
            Field(
                'venue_id', css_class="input-sm",
                id="generic-venue-id"
            ),
            Div(
                FormActions(
                    Submit('submit', _('Save'), css_class='btn-sm btn-success'),
                    css_class="col-lg-offset-2 col-lg-10"
                ),
                css_class="form-group"
            )
        )


def edit_generic_event_form_helper():
    helper = FormHelper()
    helper.form_id = 'id-edit-generic-event-info-form'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.form_method = 'post'
    helper.layout = Layout(
        Field('title', css_class="input-sm"),
        Field('description', css_class="input-sm"),
        Field(
            'start_datetime', css_class="input-sm",
            id="generic-start"
        ),
        Field(
            'end_datetime', css_class="input-sm",
            id="generic-end"
        ),
        Field(
            'venue_id', css_class="input-sm",
            id="generic-venue-id"
        ),
        Field(
            'appointment_id', css_class="input-sm",
            id="generic-appointment-id"
        ),
        Div(
            FormActions(
                Submit('submit', _('Save'), css_class='btn-sm btn-success'),
                css_class="col-lg-offset-2 col-lg-10"
            ),
            css_class="form-group"
        )
    )
    return helper


class SimpleGenericEventForm(forms.Form):

    """
    Form used to deal with events that are not appointments
    """
    start_datetime = forms.CharField(
        label=_("Start date"),
        required=True,
        widget=forms.HiddenInput
    )
    end_datetime = forms.CharField(
        label=_("End date"),
        required=False,
        widget=forms.HiddenInput
    )
    venue = forms.IntegerField(
        label=getattr(labels, 'VENUE', _("Venue")),
        required=False,
        widget=forms.HiddenInput
    )
    id = forms.IntegerField(
        label=_("Appointment"),
        required=True,
        widget=forms.HiddenInput
    )

    def save_edit(self):
        try:
            appointment = Appointment.objects.get(pk=int(self.cleaned_data['id']))
            if 'venue' in self.cleaned_data and self.cleaned_data['venue']:
                appointment.venue = Venue.objects.get(pk=self.cleaned_data['venue'])
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


class IDForm(forms.Form):

    """
    contains just the id field
    """
    id = forms.IntegerField(
        label=_("ID"),
        required=True,
        widget=forms.HiddenInput
    )


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name', 'color']

    def create_tag(self, user):
        new_tag = Tag(
            name=self.cleaned_data['name'],
            color=self.cleaned_data['color'],
            customer=user.userprofile.customer
        )
        new_tag.save()
        return new_tag

    def clean_color(self):
        value = self.cleaned_data['color']
        if value:
            value = smart_unicode(value)
            value_length = len(value)
            if value_length != 7 or not match('^\#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
                raise ValidationError(
                    _("This is an invalid color code. It must be a html hex color code e.g. #000000"))
        return value

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'tag-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name'),
            Field('color', id="id-color"),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success'),
                css_class="form-group"
            )
        )
