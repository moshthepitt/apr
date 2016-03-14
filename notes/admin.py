from django.contrib import admin

from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_filter = ['featured', 'customer', 'note_type', 'featured']
    list_display = ['note', 'customer', 'note_type', 'featured']

admin.site.register(Note, NoteAdmin)

