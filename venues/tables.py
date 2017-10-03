from django.utils.html import format_html
from django.utils.translation import ugettext as _

import django_tables2 as tables

from .models import View


class ViewTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)

    class Meta:
        model = View
        exclude = ['created_on', 'updated_on', 'id', 'customer', 'venues']
        sequence = ('name', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_action(self, record):
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>',
            record.get_edit_url(),
            record.get_delete_url()
        )
