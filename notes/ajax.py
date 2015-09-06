import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form

from notes.forms import NoteForm, EditNoteForm
from notes.models import Note
from venues.models import Venue


@csrf_exempt
@json_view
def process_add_note_form(request):
    form = NoteForm(request.POST or None)
    form.fields['venue'].queryset = Venue.objects.filter(customer=request.user.userprofile.customer)
    if form.is_valid():
        form.create_daterange_notes(request.user)
        return {
            'success': True,
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_edit_note_form(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = EditNoteForm(request.POST or None, instance=note)
    form.fields['venue'].queryset = Venue.objects.filter(customer=request.user.userprofile.customer)
    if form.is_valid():
        form.save()
        return {
            'success': True,
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    success = False
    if request.user.userprofile.customer != note.customer:
        return False
    if request.is_ajax() and request.method == 'POST':
        note.delete()
        success = True
    return HttpResponse(json.dumps(success), content_type="application/json")
