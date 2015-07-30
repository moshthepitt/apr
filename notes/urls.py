from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from notes.ajax import process_add_note_form, delete_note
from notes.views import AddNoteSnippetView, TopNotesSnippetView, BottomNotesSnippetView


urlpatterns = [
    # ajax
    url(r'^add-note-form/$', login_required(process_add_note_form), name='process_add_note_form'),
    url(r'^ajax-delete-note/(?P<pk>\d+)/$', login_required(delete_note), name='ajax_delete_note'),

    url(r'^snippet/$', login_required(AddNoteSnippetView.as_view()), name='add_note_snippet'),
    url(r'^top-notes-snippet/$', login_required(TopNotesSnippetView.as_view()), name='top_notes_snippet'),
    url(r'^bottom-notes-snippet/$', login_required(BottomNotesSnippetView.as_view()), name='bottom_notes_snippet'),

]
