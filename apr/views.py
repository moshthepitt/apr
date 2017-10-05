from urllib import urlencode

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone
from django.utils.text import slugify
from django.db import models

import pdfkit
from schedule.models import Event
from schedule.periods import Day
from dateutil import parser

from appointments.models import Tag, Appointment
from venues.models import Venue, View
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
        context['tags'] = Tag.objects.filter(
            customer=self.request.user.userprofile.customer)
        return context


class DayView(CustomerMixin, TemplateView):
    template_name = 'appointments/day_view.html'
    days_to_show = 1

    def get_context_data(self, **kwargs):
        context = super(DayView, self).get_context_data(**kwargs)
        context['venues'] = Venue.objects.filter(
            customer=self.request.user.userprofile.customer).exclude(main_calendar=False)
        context['tags'] = Tag.objects.filter(
            customer=self.request.user.userprofile.customer)
        context['days_to_show'] = self.days_to_show
        return context


ThreeDayView = DayView.as_view(
    days_to_show=3,
    template_name='appointments/three_day_view.html'
)


class PDFView(CustomerMixin, TemplateView):
    template_name = 'appointments/day-pdf.html'

    def get_data(self):
        appointments = Appointment.objects.filter(
            customer=self.customer).filter(
            event__start__day=self.date.day,
            event__start__month=self.date.month,
            event__start__year=self.date.year,
            event__end__day=self.date.day,
            event__end__month=self.date.month,
            event__end__year=self.date.year,
        )
        data = [x.serialize() for x in appointments]
        return data

    def get_context_data(self, **kwargs):
        context = super(PDFView, self).get_context_data(**kwargs)
        if not self.this_view:
            context['venues'] = Venue.objects.filter(
                customer=self.customer).exclude(main_calendar=False)
        else:
            context['venues'] = self.this_view.venues.all()
        context['tags'] = Tag.objects.filter(
            customer=self.customer)
        context['data'] = self.get_data()
        context['this_customer'] = self.customer
        context['top_notes'] = Note.objects.filter(
            customer=self.customer).exclude(featured=True).filter(
            date=self.date).filter(note_type=Note.TOP).order_by(
            'venue', '-date', 'id')
        context['top_featured_notes'] = Note.objects.filter(
            customer=self.customer).exclude(featured=False).filter(
            date=self.date).filter(note_type=Note.TOP).order_by(
            'venue', '-date', 'id')
        context['bottom_notes'] = Note.objects.filter(
            customer=self.customer).filter(
            date=self.date).filter(note_type=Note.BOTTOM).order_by(
            'venue', '-date', 'id')
        context['todays_date'] = self.date
        return context

    def dispatch(self, *args, **kwargs):
        customer_id = self.request.GET.get('cid')
        date = self.request.GET.get('date')
        self.this_view = None
        view_id = self.request.GET.get('view_id')

        if view_id:
            try:
                view_id = int(view_id)
            except TypeError:
                pass
            except ValueError:
                pass
            else:
                try:
                    self.this_view = View.objects.get(pk=view_id)
                except View.DoesNotExist:
                    pass

        if customer_id and date:
            try:
                self.customer = get_object_or_404(Customer, pk=customer_id)
            except ValueError:
                raise Http404
            try:
                self.date = parser.parse(date).date()
            except ValueError:
                self.date = timezone.now().date()
        else:
            raise Http404

        return super(PDFView, self).dispatch(*args, **kwargs)


def generate_pdf_view(request):
    data = {
        'date': request.GET.get('date'),
        'cid': request.user.userprofile.customer.pk,
        'view_id': request.GET.get('view_id'),
    }
    url = request.build_absolute_uri(
        reverse('secret_pdf')) + "?" + urlencode(data)
    filename = slugify("{} {}".format(
        request.user.userprofile.customer.name, data['date'])) + ".pdf"

    options = {
        'dpi': 300,
        'viewport-size': '900',
        'encoding': "UTF-8",
        'no-outline': None
    }

    pdf = pdfkit.from_url(url, False, options=options)

    # set HTTP response headers
    response = HttpResponse(content_type="application/pdf")
    response["Cache-Control"] = "max-age=0"
    response["Accept-Ranges"] = "none"
    response["Content-Disposition"] =\
        "attachment; filename={}".format(filename)

    # send the generated PDF
    response.write(pdf)

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
        if self.request.user.is_authenticated and\
                self.request.user.userprofile.customer:
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


class ErrorView(TemplateView):
    template_name = 'core/error.html'
