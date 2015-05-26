from doctors.models import Doctor


def doctor_processor(request):
    if request.user.is_authenticated():
        result = Doctor.objects.filter(customer=request.user.userprofile.customer).exclude(is_active=False)
    else:
        result = []
    return {'active_doctors': result}
