
def current_customer_processor(request):
    if request.user.is_authenticated():
        customer = request.user.userprofile.customer
        return {'CUSTOMER': customer}
    return {'CUSTOMER': None}
