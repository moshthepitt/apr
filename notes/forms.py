from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import Field, FormActions
from dateutil.rrule import rrule, DAILY

from notes.models import Note


class NoteForm(forms.ModelForm):
    end_date = forms.DateField(
        label=_('End date'),
        input_formats=["%d-%m-%Y"],
        help_text=_(
            "If specified, the note will be created for all dates from the current date through to the End Date selected")
    )

    class Meta:
        model = Note
        fields = ['date', 'venue', 'note', 'note_type', 'featured']

    def clean_end_date(self):
        if self.cleaned_data['end_date'] < self.cleaned_data['date']:
            raise forms.ValidationError(_("The end date cannot be in the past"))
        return self.cleaned_data['end_date']

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
            Field('featured'),
            Field('end_date', id="end-date"),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )

    def create_note(self, user):
        new_note = Note(
            date=self.cleaned_data['date'],
            venue=self.cleaned_data['venue'],
            note=self.cleaned_data['note'],
            note_type=self.cleaned_data['note_type'],
            featured=self.cleaned_data['featured'],
            creator=user,
            customer=user.userprofile.customer
        )
        new_note.save()
        return new_note

    def create_daterange_notes(self, user):
        end_date = self.cleaned_data['end_date']
        date = self.cleaned_data['date']
        if date == end_date:
            return self.create_note(user)
        else:
            for x in rrule(DAILY, dtstart=date, until=end_date):
                new_note = Note(
                    date=x,
                    venue=self.cleaned_data['venue'],
                    note=self.cleaned_data['note'],
                    note_type=self.cleaned_data['note_type'],
                    featured=self.cleaned_data['featured'],
                    creator=user,
                    customer=user.userprofile.customer
                )
                new_note.save()
            return True


class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['date', 'venue', 'note', 'note_type', 'featured']

    def __init__(self, *args, **kwargs):
        super(EditNoteForm, self).__init__(*args, **kwargs)
        self.fields['venue'].required = True
        self.fields['date'].widget = forms.HiddenInput()
        self.fields['note'].widget = forms.TextInput()
        self.helper = FormHelper()
        self.helper.form_id = 'id-edit-note-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('date'),
            Field('venue', id="id-select-venue"),
            Field('note'),
            Field('note_type'),
            Field('featured'),
            FormActions(
                Submit('submit', _('Save'), css_class='btn-success')
            )
        )
