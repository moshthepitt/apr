# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field

from venues.models import Venue


class VenueForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = ['name', 'main_calendar', 'shown_days', 'allow_overlap', 'send_sms', 'send_email']

    def create_venue(self, user):
        new_venue = Venue(
            name=self.cleaned_data['name'],
            main_calendar=self.cleaned_data['main_calendar'],
            creator=user,
            customer=user.userprofile.customer
        )
        new_venue.save()
        return new_venue

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'schedule-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name'),
            Field('main_calendar'),
            Field('shown_days'),
            Field('allow_overlap'),
            Field('send_sms'),
            Field('send_email'),
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )


class NoSubmitVenueFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(NoSubmitVenueFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_id = 'schedule-form'
        self.form_method = 'post'
        self.layout = Layout(
            Field('name'),
            Field('shown_days'),
            Field('allow_overlap'),
            Field('send_sms'),
            Field('send_email'),
            Field('main_calendar'),
        )


class VenueScriptForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = ['custom_reminder', 'reminder_sender', 'reminder_subject',
                  'reminder_email', 'reminder_sms', 'show_confirm_link', 'show_cancel_link']

    def __init__(self, *args, **kwargs):
        super(VenueScriptForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-venue-script-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('custom_reminder'),
            Field('reminder_sender'),
            Field('reminder_subject'),
            Field('reminder_email'),
            Field('reminder_sms'),
            Field('show_confirm_link'),
            Field('show_cancel_link'),
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )
