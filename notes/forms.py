from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit

from notes.models import Note


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['date', 'venue', 'note', 'note_type']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['venue'].required = True
        self.fields['date'].widget = forms.HiddenInput()
        self.fields['note'].widget = forms.TextInput()
        self.helper = FormHelper()
        self.helper.form_id = 'id-note-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('date'),
            Field('venue', id="id-select-venue"),
            Field('note'),
            Field('note_type'),
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )

    def create_note(self, user):
        new_note = Note(
            date=self.cleaned_data['date'],
            venue=self.cleaned_data['venue'],
            note=self.cleaned_data['note'],
            note_type=self.cleaned_data['note_type'],
            creator=user,
            customer=user.userprofile.customer
        )
        new_note.save()
        return new_note
