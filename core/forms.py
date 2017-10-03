from django import forms
from django.utils.translation import ugettext as _
from core.emails import send_feedback_email

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions, Field, FieldWithButtons


class SupportForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={'rows': 5}))
    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)

    def send_email(self):
        # try to trick spammers by checking whether the honeypot field is
        # filled in; not super complicated/effective but it works
        if self.cleaned_data['honeypot']:
            return False
        send_feedback_email(
            self.cleaned_data['email'], self.cleaned_data['message'])

    def __init__(self, *args, **kwargs):
        super(SupportForm, self).__init__(*args, **kwargs)
        # crispy forms stuff
        self.helper = FormHelper()
        self.helper.render_hidden_fields = True
        self.helper.form_id = 'id-support-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                _('Send us an email'),
                'email',
                'message',
                'honeypot'
            ),
            FormActions(
                Submit('submit', _('Send'), css_class='btn-primary')
            )
        )


class ListViewSearchForm(forms.Form):
    q = forms.CharField(label=_("Search Query"), required=False)

    def __init__(self, *args, **kwargs):
        super(ListViewSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'get'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = False
        self.helper.html5_required = True
        self.helper.form_id = 'search-form'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            FieldWithButtons(
                Field('q', css_class="input-sm"),
                Submit('submitBtn', _('Search'), css_class='btn-sm')
            ),
        )
