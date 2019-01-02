from dateutil import parser

from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.utils import timezone

from venues.models import Venue, View
from notes.forms import NoteForm, EditNoteForm
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
            date = timezone.localtime(parser.parse(input_date)).date()
        else:
            date = timezone.now().date()

        note_form = NoteForm()
        if not self.this_view:
            note_form.fields['venue'].queryset = Venue.objects.filter(
                customer=self.request.user.userprofile.customer).exclude(
                main_calendar=False)
        else:
            note_form.fields['venue'].queryset = self.this_view.venues.all()
        note_form.fields['date'].initial = date
        note_form.fields['end_date'].initial = date.strftime("%d-%m-%Y")
        context['NoteForm'] = note_form
        return context

    def dispatch(self, *args, **kwargs):
        self.this_view = None
        if self.request.GET.get('view_id'):
            try:
                self.this_view = View.objects.get(
                    pk=self.request.GET.get('view_id'))
            except View.DoesNotExist:
                pass
            except ValueError:
                pass
        return super(AddNoteSnippetView, self).dispatch(*args, **kwargs)


class EditNoteSnippetView(Customer404Mixin, TemplateView):

    """
    returns modal content when adding new appointment
    """
    template_name = "notes/snippets/edit-note.html"

    def get_context_data(self, **kwargs):
        context = super(EditNoteSnippetView, self).get_context_data(**kwargs)
        note_form = EditNoteForm(instance=self.object)
        context['NoteForm'] = note_form
        context['object'] = self.object
        return context

    def dispatch(self, *args, **kwargs):
        self.object = get_object_or_404(Note, pk=self.kwargs['pk'])
        return super(EditNoteSnippetView, self).dispatch(*args, **kwargs)


class TopNotesSnippetView(Customer404Mixin, TemplateView):
    template_name = "notes/snippets/top-notes.html"
    model = Note
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(TopNotesSnippetView, self).get_context_data(**kwargs)
        input_date = self.request.GET.get('date', "")
        if input_date:
            date = timezone.localtime(parser.parse(input_date)).date()
        else:
            date = timezone.now().date()
        context['notes'] = Note.objects.filter(
            customer=self.request.user.userprofile.customer).exclude(
            featured=True).filter(
            date=date).filter(note_type=Note.TOP).order_by(
            'venue', '-date', 'id')
        if not self.this_view:
            context['venues'] = Venue.objects.filter(
                customer=self.request.user.userprofile.customer).exclude(
                main_calendar=False)
        else:
            context['venues'] = self.this_view.venues.all()
        return context

    def dispatch(self, *args, **kwargs):
        self.this_view = None
        if self.request.GET.get('view_id'):
            try:
                self.this_view = View.objects.get(
                    pk=self.request.GET.get('view_id'))
            except View.DoesNotExist:
                pass
            except ValueError:
                pass
        return super(TopNotesSnippetView, self).dispatch(*args, **kwargs)


class TopFeaturedNotesSnippetView(Customer404Mixin, TemplateView):
    template_name = "notes/snippets/top-featured-notes.html"
    model = Note
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(TopFeaturedNotesSnippetView, self).get_context_data(
            **kwargs)
        input_date = self.request.GET.get('date', "")
        if input_date:
            date = timezone.localtime(parser.parse(input_date)).date()
        else:
            date = timezone.now().date()
        context['notes'] = Note.objects.filter(
            customer=self.request.user.userprofile.customer).exclude(
            featured=False).filter(
            date=date).filter(note_type=Note.TOP).order_by(
            'venue', '-date', 'id')
        if not self.this_view:
            context['venues'] = Venue.objects.filter(
                customer=self.request.user.userprofile.customer).exclude(
                main_calendar=False)
        else:
            context['venues'] = self.this_view.venues.all()
        return context

    def dispatch(self, *args, **kwargs):
        self.this_view = None
        if self.request.GET.get('view_id'):
            try:
                self.this_view = View.objects.get(
                    pk=self.request.GET.get('view_id'))
            except View.DoesNotExist:
                pass
            except ValueError:
                pass
        return super(TopFeaturedNotesSnippetView, self).dispatch(
            *args, **kwargs)


class BottomNotesSnippetView(Customer404Mixin, TemplateView):
    template_name = "notes/snippets/bottom-notes.html"
    model = Note
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(BottomNotesSnippetView, self).get_context_data(
            **kwargs)
        input_date = self.request.GET.get('date', "")
        if input_date:
            date = timezone.localtime(parser.parse(input_date)).date()
        else:
            date = timezone.now().date()
        context['notes'] = Note.objects.filter(
            customer=self.request.user.userprofile.customer).filter(
            date=date).filter(note_type=Note.BOTTOM).order_by(
            'venue', '-date', 'id')
        if not self.this_view:
            context['venues'] = Venue.objects.filter(
                customer=self.request.user.userprofile.customer).exclude(
                main_calendar=False)
        else:
            context['venues'] = self.this_view.venues.all()
        return context

    def dispatch(self, *args, **kwargs):
        self.this_view = None
        if self.request.GET.get('view_id'):
            try:
                self.this_view = View.objects.get(
                    pk=self.request.GET.get('view_id'))
            except View.DoesNotExist:
                pass
            except ValueError:
                pass
        return super(BottomNotesSnippetView, self).dispatch(*args, **kwargs)
