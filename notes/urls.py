from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from notes.ajax import (delete_note, process_add_note_form,
                        process_edit_note_form)
from notes.views import (AddNoteSnippetView, BottomNotesSnippetView,
                         EditNoteSnippetView, TopFeaturedNotesSnippetView,
                         TopNotesSnippetView)

urlpatterns = [
    # ajax
    url(r'^add-note-form/',
        login_required(process_add_note_form),
        name='process_add_note_form'),
    url(r'^edit-note-form/(?P<pk>\d+)/',
        login_required(process_edit_note_form),
        name='process_edit_note_form'),
    url(r'^ajax-delete-note/(?P<pk>\d+)/',
        login_required(delete_note),
        name='ajax_delete_note'),
    url(r'^snippet/',
        login_required(AddNoteSnippetView.as_view()),
        name='add_note_snippet'),
    url(r'^edit-note-snippet/(?P<pk>\d+)/',
        login_required(EditNoteSnippetView.as_view()),
        name='edit_note_snippet'),
    url(r'^top-notes-snippet/',
        login_required(TopNotesSnippetView.as_view()),
        name='top_notes_snippet'),
    url(r'^top-featured-notes-snippet/',
        login_required(TopFeaturedNotesSnippetView.as_view()),
        name='top_featured_notes_snippet'),
    url(r'^bottom-notes-snippet/',
        login_required(BottomNotesSnippetView.as_view()),
        name='bottom_notes_snippet'), ]
