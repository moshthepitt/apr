from django.shortcuts import redirect
from django.http import Http404
from django.contrib import messages
from django.utils.translation import ugettext as _


class CustomerMixin(object):

    """
    Alters view behaviour based on Customer
        if customer does not exist then redirect to new customer signup page
        if customer exists but has no active subscription redirect to upgrade
        page
        if customer has no active subscription then we need to make them pay
    """
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            # if current user is not tied to a customer then redirect them away
            if not self.request.user.userprofile.customer:
                messages.add_message(
                    self.request, messages.INFO, _('Please set up your account'
                                                   ' to get started'))
                return redirect('new_customer')
            # if current user is not tied to a subscription then redirect them
            # away
            if not self.request.user.userprofile.customer.has_subscription():
                messages.add_message(
                    self.request, messages.INFO, _('Please set up your account'
                                                   ' to get started'))
                return redirect('new_customer')
            # if subscription not active redirect to payment page
            customer = self.request.user.userprofile.customer
            if not customer.customersubscription.active:
                messages.add_message(self.request, messages.INFO, _(
                    'Your account is not active, please make a payment to '
                    'activate it.'))
                return redirect('customer:subscription')
        return super(CustomerMixin, self).dispatch(*args, **kwargs)


class Customer404Mixin(object):

    """
    Like CustomerMixin but raises Http404 is wrong/no customer
    """
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            # if current user is not tied to a customer then redirect them away
            if not self.request.user.userprofile.customer:
                raise Http404
            # if current user is not tied to a subscription then redirect them
            # away
            if not self.request.user.userprofile.customer.has_subscription():
                raise Http404
            # if subscription not active redirect to payment page
            if not self.request.user.userprofile.customer.customersubscription.active:
                raise Http404
        return super(Customer404Mixin, self).dispatch(*args, **kwargs)


class LesserCustomerMixin(object):

    """
    Like CustomerMixin but raises Http404 is wrong/no customer but does not
    check if sub is active
    """
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            # if current user is not tied to a customer then redirect them away
            if not self.request.user.userprofile.customer:
                return redirect('new_customer')
            # if current user is not tied to a subscription then redirect them
            # away
            if not self.request.user.userprofile.customer.has_subscription():
                return redirect('new_customer')
        return super(LesserCustomerMixin, self).dispatch(*args, **kwargs)


class CustomerExistsMixin(object):
    """
    Used to make sure the user has a valid customer
    """
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if not self.request.user.userprofile.customer:
                raise Http404
        return super(CustomerExistsMixin, self).dispatch(*args, **kwargs)


class CustomerFilterMixin(object):
    """
    Modifies the Queryset to flter items by current customer
    """

    def get_queryset(self):
        queryset = super(CustomerFilterMixin, self).get_queryset()
        return queryset.filter(customer=self.request.user.userprofile.customer)


class CustomerFormMixin(object):
    """
    Used in form views for forms that need an initial customer
    """

    def get_initial(self):
        initial = super(CustomerFormMixin, self).get_initial()
        initial['customer'] = self.request.user.userprofile.customer
        return initial
