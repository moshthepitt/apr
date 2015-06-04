# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

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


class OpeningHourFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(OpeningHourFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_method = 'post'
        self.layout = Layout(
            Field('weekday', readonly=True, disabled=True),
            Field('from_hour'),
            Field('to_hour'),
        )
        self.render_required_fields = True
        self.template = 'bootstrap/table_inline_formset.html'
