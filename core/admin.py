from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from suit_redactor.widgets import RedactorWidget


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': RedactorWidget(editor_options={'lang': 'en'})}
    }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)
