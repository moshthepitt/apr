from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages

from braces.views import LoginRequiredMixin, FormMessagesMixin
from django_tables2 import SingleTableView

from core.mixins import CoreFormMixin, ListViewSearchMixin, VerboseNameMixin
from customers.mixins import CustomerFormMixin, CustomerMixin
from customers.mixins import CustomerFilterMixin


class CoreListView(LoginRequiredMixin, CustomerMixin,
                   CustomerFilterMixin, VerboseNameMixin, ListViewSearchMixin,
                   SingleTableView, ListView):
    template_name = "core/crud/list.html"


class CoreCreateView(LoginRequiredMixin, CustomerMixin,
                     FormMessagesMixin, VerboseNameMixin, CoreFormMixin,
                     CustomerFormMixin, CreateView):
    template_name = "core/crud/create.html"
    form_valid_message = _("Saved successfully!")
    form_invalid_message = _("Please correct the errors below.")


class CoreUpdateView(LoginRequiredMixin, FormMessagesMixin,
                     VerboseNameMixin, CoreFormMixin, UpdateView):
    template_name = "core/crud/edit.html"
    form_valid_message = _("Saved successfully!")
    form_invalid_message = _("Please correct the errors below.")


class CoreGenericDeleteView(LoginRequiredMixin, FormMessagesMixin,
                            VerboseNameMixin, DeleteView):
    template_name = "core/crud/delete.html"
    form_valid_message = _("Deleted successfully!")
    form_invalid_message = _("Please correct the errors below.")


class CoreDeleteView(CoreGenericDeleteView):

    def delete(self, request, *args, **kwargs):
        try:
            return super(CoreDeleteView, self).delete(request, *args, **kwargs)
        except ProtectedError:
            info = _("You cannot delete this item, it is referenced by other "
                     "items.")
            messages.error(request, info, fail_silently=True)
            return redirect(self.object.get_delete_url())
