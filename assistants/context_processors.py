from assistants.models import Assistant


def assistant_processor(request):
    return {'active_assistants': Assistant.objects.exclude(is_active=False)}
