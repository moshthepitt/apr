from dateutil import parser

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.utils import timezone
# from django.http import Http404

from venues.models import Venue
from notes.forms import NoteForm
from notes.models import Note
from customers.mixins import Customer404Mixin


class AddNoteSnippetView(Customer404Mixin, TemplateView):

    """
    returns modal content when adding new appointment
    """
    template_name = "notes/snippets/add-note.html"

    def get_context_data(self, **kwargs):
        context = super(AddNoteSnippetView, self).get_context_data(**kwargs)

        input_date = self.request.GET.get('date', "")
        if input_date:
            date = timezone.localtime(parser.parse(input_date)).date
        else:
            date = timezone.now().date

        note_form = NoteForm()
        note_form.fields['venue'].queryset = Venue.objects.filter(
            customer=self.request.user.userprofile.customer)
        note_form.fields['date'].initial = date
        context['NoteForm'] = note_form
        return context


class TopNotesSnippetView(Customer404Mixin, TemplateView):
    template_name = "notes/snippets/top-notes.html"
    model = Note
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(TopNotesSnippetView, self).get_context_data(**kwargs)
        input_date = self.request.GET.get('date', "")
        if input_date:
            date = timezone.localtime(parser.parse(input_date)).date
        else:
            date = timezone.now().date
        context['notes'] = Note.objects.filter(customer=self.request.user.userprofile.customer).filter(
            date=date).filter(note_type=Note.TOP).order_by('venue', '-date', 'id')
        context['venues'] = Venue.objects.filter(customer=self.request.user.userprofile.customer).exclude(main_calendar=False)
        return context


class BottomNotesSnippetView(Customer404Mixin, TemplateView):
    template_name = "notes/snippets/bottom-notes.html"
    model = Note
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(BottomNotesSnippetView, self).get_context_data(**kwargs)
        input_date = self.request.GET.get('date', "")
        if input_date:
            date = timezone.localtime(parser.parse(input_date)).date
        else:
            date = timezone.now().date
        context['notes'] = Note.objects.filter(customer=self.request.user.userprofile.customer).filter(
            date=date).filter(note_type=Note.BOTTOM).order_by('venue', '-date', 'id')
        context['venues'] = Venue.objects.filter(customer=self.request.user.userprofile.customer).exclude(main_calendar=False)
        return context
