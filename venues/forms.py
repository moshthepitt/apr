# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field

from venues.models import Venue


class VenueForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = ['name']

    def create_venue(self, user):
        new_venue = Venue(
            name=self.cleaned_data['name'],
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
        )
