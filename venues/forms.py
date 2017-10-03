# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions

from customers.models import Customer
from venues.models import Venue, View


class VenueForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = ['name',
                  'main_calendar',
                  'shown_days',
                  'allow_overlap',
                  'send_sms',
                  'send_email',
                  'client_display']

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
            Field('shown_days'),
            Field('client_display'),
            Field('main_calendar'),
            Field('allow_overlap'),
            Field('send_sms'),
            Field('send_email'),
            FormActions(
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
            Field('client_display'),
            Field('main_calendar'),
            Field('allow_overlap'),
            Field('send_sms'),
            Field('send_email'),
        )


class VenueScriptForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = ['custom_reminder', 'reminder_sender', 'reminder_subject',
                  'reminder_email', 'reminder_sms', 'show_confirm_link',
                  'show_cancel_link']

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
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )


class ViewForm(forms.ModelForm):

    class Meta:
        model = View
        fields = [
            'name',
            'venues',
            'customer',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ViewForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
            self.fields['venues'].queryset = Venue.objects.filter(
                customer__id__in=[self.request.user.userprofile.customer.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'view-form'
        self.helper.layout = Layout(
            Field('name'),
            Field('venues'),
            Field('customer', type="hidden"),
            FormActions(
                Submit('submitBtn',
                       _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>"
                    "".format(
                        reverse('venues:views_list'), _("Back")))
            )
        )
