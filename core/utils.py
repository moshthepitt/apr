from django.core.cache import cache
from django.utils import timezone
from django.core.cache.utils import make_template_fragment_key


def invalidate_caches(name, param_list):
    key = make_template_fragment_key(name, param_list)
    cache.delete(key)


def replace_script_variables(some_string, appointment):
    """
    does string replacement for all our custom variables:
        $NAME The client's name (e.g. John Doe).
        $FIRST_NAME The client's first name (e.g. John).
        $OUR_NAME The client-friendly name of the facility the appointment is at (e.g. Surri Inc).
        $OUR_PHONE The phone number of the facility the appointment is at
        $APPOINTMENT_DATE The date of the appointment (e.g. Sunday, June 7th)
        $APPOINTMENT_START_TIME The time of the appointment (e.g. 9a.m.)
    """
    start_time = timezone.localtime(appointment.event.start)

    some_string = some_string.replace("$NAME", appointment.client.get_full_name().strip())
    some_string = some_string.replace("$FIRST_NAME", appointment.client.first_name.strip())
    some_string = some_string.replace("$OUR_NAME", appointment.customer.name.strip())
    some_string = some_string.replace("$OUR_PHONE", appointment.customer.phone.as_e164)
    some_string = some_string.replace("$APPOINTMENT_DATE", start_time.strftime("%A, %B %-d"))
    some_string = some_string.replace("$APPOINTMENT_START_TIME", start_time.strftime("%-I%p"))
    return some_string


def replace_client_script_variables(some_string, client):
    """
    does string replacement for all our custom variables:
        $NAME The client's name (e.g. John Doe).
        $FIRST_NAME The client's first name (e.g. John).
        $OUR_NAME The client-friendly name of the facility the appointment is at (e.g. Surri Inc).
        $OUR_PHONE The phone number of the facility the appointment is at
    """
    some_string = some_string.replace("$NAME", client.get_full_name().strip())
    some_string = some_string.replace("$FIRST_NAME", client.first_name.strip())
    some_string = some_string.replace("$OUR_NAME", client.customer.name.strip())
    some_string = some_string.replace("$OUR_PHONE", client.customer.phone.as_e164)
    return some_string
