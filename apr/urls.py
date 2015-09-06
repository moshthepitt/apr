from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

from apr.views import HomeView, DashboardView, CustomerRedirect, DayView, PricingView
from apr.views import SupportView, generate_pdf_view, PDFView, ErrorView, ThreeDayView
from appointments.views import AppointmentClientConfirm, AppointmentClientCancel
from customers.views import NewCustomer

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^pricing/$', PricingView.as_view(), name='pricing'),
    url(r'^support/$', SupportView.as_view(), name='support'),
    url(r'^error/$', ErrorView.as_view(), name='error'),
    url(r'^help/$', SupportView.as_view(template_name="core/help.html"), name='help'),
    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),
    url(r'^day/$', login_required(DayView.as_view()), name='day'),
    url(r'^three-day/$', login_required(ThreeDayView), name='four_day'),
    url(r'^pdf/$', login_required(generate_pdf_view), name='pdf'),
    url(r'^new/$', login_required(NewCustomer.as_view()), name='new_customer'),
    url(r'^appointments/', include('appointments.urls', namespace='appointments')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^schedules/', include('venues.urls', namespace='venues')),
    url(r'^customer/', include('customers.urls', namespace='customer')),
    url(r'^notes/', include('notes.urls', namespace='notes')),

    url(r'^WeAreGoingToIbiza2015/$', PDFView.as_view(), name='secret_pdf'),

    url(r'^admin/', include(admin.site.urls)),

    # third party
    url(r'^select2/', include('django_select2.urls')),
    url(r'^accounts/', include('allauth.urls')),

    # utils
    url(r'^customer-redirector/$', CustomerRedirect.as_view(), name='customer_redirect'),

    # client actions
    url(r'^confirm/(?P<slug>[\w-]+)/$', AppointmentClientConfirm.as_view(), name='confirm_appointment'),
    url(r'^cancel/(?P<slug>[\w-]+)/$', AppointmentClientCancel.as_view(), name='cancel_appointment'),

    # flat pages
    url(r'^$', include('django.contrib.flatpages.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
