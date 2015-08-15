from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone

import pdfcrowd
from schedule.models import Event
from schedule.periods import Period

from venues.models import Venue
from subscriptions.models import Subscription
from core.forms import SupportForm
from customers.models import Customer
from customers.mixins import CustomerMixin
from notes.models import Note


class DashboardView(CustomerMixin, TemplateView):
    template_name = 'appointments/calendar.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(
            customer=self.request.user.userprofile.customer).exclude(main_calendar=False)
        return context


class DayView(CustomerMixin, TemplateView):
    template_name = 'appointments/day_view.html'

    def get_context_data(self, **kwargs):
        context = super(DayView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(
            customer=self.request.user.userprofile.customer).exclude(main_calendar=False)
        return context


class PDFView(CustomerMixin, TemplateView):
    template_name = 'appointments/day-pdf.html'

    def get_data(self):
        period = Period(Event.objects.exclude(appointment=None).filter(
            appointment__customer=self.customer), self.fro, self.to)
        data = [{'id': x.event.appointment_set.first().pk,
                 'title': "{}".format(x.event.appointment_set.first().client.display_name(title=x.event.title)),
                 'userId': [x.event.appointment_set.first().venue.pk],
                 'start': x.start.isoformat(),
                 'end': x.end.isoformat(),
                 'clientId': x.event.appointment_set.first().client.pk,
                 'status': x.event.appointment_set.first().status,
                 'body': x.event.description
                 }
                for x in period.get_occurrences()]
        return data

    def get_context_data(self, **kwargs):
        context = super(PDFView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(
            customer=self.customer).exclude(main_calendar=False)
        context['data'] = self.get_data()
        context['this_customer'] = self.customer
        context['top_notes'] = Note.objects.filter(customer=self.customer).filter(
            date=self.date).filter(note_type=Note.TOP).order_by('venue', '-date', 'id')
        context['bottom_notes'] = Note.objects.filter(customer=self.customer).filter(
            date=self.date).filter(note_type=Note.BOTTOM).order_by('venue', '-date', 'id')
        return context

    def dispatch(self, *args, **kwargs):
        customer_id = self.request.GET.get('cid')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        if not customer_id or not start or not end:
            raise Http404
        self.customer = get_object_or_404(Customer, pk=customer_id)
        self.fro = timezone.make_aware(
            datetime.fromtimestamp(float(start)), timezone.get_current_timezone())
        self.to = timezone.make_aware(
            datetime.fromtimestamp(float(end)), timezone.get_current_timezone())
        self.date = timezone.localtime(self.fro).date
        return super(PDFView, self).dispatch(*args, **kwargs)


def generate_pdf_view(request):
    try:
        # create an API client instance
        client = pdfcrowd.Client("moshthepitt", "cf5b6d7c0874852f662131f02dd4a1ac")

        # convert a web page and store the generated PDF to a variable
        data = {
            'venues': Venue.objects.filter(customer=request.user.userprofile.customer).exclude(main_calendar=False)
        }
        html = render_to_string('appointments/day-pdf.html', data, context_instance=RequestContext(request))

        pdf = client.convertHtml(html)

        # set HTTP response headers
        response = HttpResponse(content_type="application/pdf")
        response["Cache-Control"] = "max-age=0"
        response["Accept-Ranges"] = "none"
        response["Content-Disposition"] = "attachment; filename=google_com.pdf"

        # send the generated PDF
        response.write(pdf)
    except pdfcrowd.Error, why:
        response = HttpResponse(content_type="text/plain")
        response.write(why)
    return response


class HomeView(TemplateView):
    template_name = 'core/home.html'


class PricingView(ListView):
    template_name = 'core/pricing.html'
    model = Subscription

    def get_queryset(self):
        queryset = Subscription.objects.exclude(highlighted=False)
        return queryset


class CustomerRedirect(RedirectView):

    """
    This view tries to redirect you to the right customer if possible
    """
    permanent = False
    query_string = True
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.userprofile.customer:
            return reverse_lazy('dashboard')
        return super(CustomerRedirect, self).get_redirect_url(*args, **kwargs)


class SupportView(FormView):
    template_name = 'core/support.html'
    form_class = SupportForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully sent email'))
        return super(SupportView, self).form_valid(form)
