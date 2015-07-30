from django.views.decorators.csrf import csrf_exempt

from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form

from notes.forms import NoteForm
from venues.models import Venue


@csrf_exempt
@json_view
def process_add_note_form(request):
    form = NoteForm(request.POST or None)
    form.fields['venue'].queryset = Venue.objects.filter(customer=request.user.userprofile.customer)
    if form.is_valid():
        form.create_note(request.user)
        return {
            'success': True,
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}
