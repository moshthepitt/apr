from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from customers.views import EditCustomer

urlpatterns = patterns('',
    url(r'^edit/$', login_required(EditCustomer.as_view()), name='edit'),
)
