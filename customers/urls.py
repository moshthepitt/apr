from customers.views import (EditCustomer, EditCustomerBirthdayGreetings,
                             EditCustomerRebooking, EditCustomerScript,
                             EditCustomerSettings, PayView, PlanView,
                             SubscriptionListView)
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^edit/', login_required(EditCustomer.as_view()), name='edit'),
    url(r'^script/',
        login_required(EditCustomerScript.as_view()),
        name='script'),
    url(r'^birthday/',
        login_required(EditCustomerBirthdayGreetings.as_view()),
        name='birthday'),
    url(r'^rebooking/',
        login_required(EditCustomerRebooking.as_view()),
        name='rebooking'),
    url(r'^settings/',
        login_required(EditCustomerSettings.as_view()),
        name='settings'),
    url(r'^subscription/',
        login_required(SubscriptionListView.as_view()),
        name='subscription'),
    url(r'^pay/', login_required(PayView.as_view()), name='pay'),
    url(r'^plan/(?P<pk>\d+)/', login_required(PlanView.as_view()),
        name='plan'),
]
