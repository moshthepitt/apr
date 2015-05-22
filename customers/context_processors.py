
def current_customer_processor(request):
    customer = request.user.userprofile.customer
    return {'CUSTOMER': customer}
