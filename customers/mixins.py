from django.shortcuts import redirect


class CustomerMixin(object):
    """
    Alters view behaviour based on Customer
        if customer does not exist then redirect to new customer signup page
        if customer exists but has no active subscription redirect to upgrade page
    """

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            # if current user is not tied to a customer then redirect them away
            if not self.request.user.userprofile.customer:
                return redirect('new_customer')
            # if current user is not tied to a subscription then redirect them away
            if not self.request.user.userprofile.customer.customersubscription.subscription:
                return redirect('new_customer')
        return super(CustomerMixin, self).dispatch(*args, **kwargs)
