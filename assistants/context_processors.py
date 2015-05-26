from assistants.models import Assistant


def assistant_processor(request):
    if request.user.is_authenticated():
        result = Assistant.objects.filter(customer=request.user.userprofile.customer).exclude(is_active=False)
    else:
        result = []
    return {'active_assistants': result}
