# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import Field

from venues.models import Venue
from opening_hours.models import OpeningHour


class OpeningHourFormSetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(OpeningHourFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_method = 'post'
        self.layout = Layout(
            Field('weekday', disabled=True),
            Field('from_hour'),
            Field('to_hour'),
        )
        self.render_required_fields = True
        self.template = 'bootstrap3/table_inline_formset.html'


class OpeningHourForm(forms.ModelForm):

    class Meta:
        model = OpeningHour
        fields = ['weekday', 'from_hour', 'to_hour']

    def __init__(self, *args, **kwargs):
        super(OpeningHourForm, self).__init__(*args, **kwargs)
        self.fields['weekday'].required = False
        self.fields['from_hour'].required = False
        self.fields['to_hour'].required = False

    def clean_weekday(self):
        if self.instance and self.instance.pk:
            return self.instance.weekday
        else:
            return self.cleaned_data['weekday']


OpeningHourFormSet = inlineformset_factory(
    Venue, OpeningHour, form=OpeningHourForm, can_delete=False, extra=0)
