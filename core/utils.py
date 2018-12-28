import csv

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone

from users.models import Client
from dateutil import parser
from phonenumber_field.validators import validate_international_phonenumber


def invalidate_caches(name, param_list):
    key = make_template_fragment_key(name, param_list)
    cache.delete(key)


def replace_script_variables(some_string, appointment):
    """
    does string replacement for all our custom variables:
        $NAME The client's name (e.g. John Doe).
        $FIRST_NAME The client's first name (e.g. John).
        $OUR_NAME The client-friendly name of the facility the appointment
                  is at (e.g. Surri Inc).
        $OUR_PHONE The phone number of the facility the appointment is at
        $APPOINTMENT_DATE The date of the appointment (e.g. Sunday, June 7th)
        $APPOINTMENT_START_TIME The time of the appointment (e.g. 9a.m.)
    """
    start_time = timezone.localtime(appointment.event.start)

    some_string = some_string.replace(
        "$NAME",
        appointment.client.get_full_name().strip())
    some_string = some_string.replace("$FIRST_NAME",
                                      appointment.client.first_name.strip())
    some_string = some_string.replace("$OUR_NAME",
                                      appointment.customer.name.strip())
    some_string = some_string.replace("$OUR_PHONE",
                                      appointment.customer.phone.as_e164)
    some_string = some_string.replace("$APPOINTMENT_DATE",
                                      start_time.strftime("%A, %B %-d"))
    some_string = some_string.replace("$APPOINTMENT_START_TIME",
                                      start_time.strftime("%-I:%M%p"))
    return some_string


def replace_client_script_variables(some_string, client):
    """
    does string replacement for all our custom variables:
        $NAME The client's name (e.g. John Doe).
        $FIRST_NAME The client's first name (e.g. John).
        $OUR_NAME The client-friendly name of the facility the appointment
                  is at (e.g. Surri Inc).
        $OUR_PHONE The phone number of the facility the appointment is at
    """
    some_string = some_string.replace("$NAME", client.get_full_name().strip())
    some_string = some_string.replace("$FIRST_NAME", client.first_name.strip())
    some_string = some_string.replace("$OUR_NAME",
                                      client.customer.name.strip())
    some_string = some_string.replace("$OUR_PHONE",
                                      client.customer.phone.as_e164)
    return some_string


def import_clientsdb(filename, customer, creator):
    """Import clients database"""
    with open(filename, "rb") as ifile:
        reader = csv.reader(ifile)
        t = zip(reader)
    import_list = [x[0] for x in t]
    for i, row in enumerate(import_list):
        client_id = row[0].strip()
        if client_id:
            names = row[1].strip()
            dob = row[2].strip()
            adult_dependant = row[3].strip()
            phone = row[4].strip()
            other_phone = row[5].strip()
            email = row[6].strip()
            address = row[7].strip()
            date_first_appt = row[8].strip()
            notes = row[9].strip()
            next_of_kin = row[10].strip()
            next_of_kin_relationship = row[11].strip()
            next_of_kin_phone = row[12].strip()

            names_list = names.split(" ")
            first_name = names_list[0]
            last_name = names_list[-1]
            other_names = ""
            if len(names_list) > 2:
                other_names = names_list[1:-1]

            try:
                birthdate = parser.parse(dob).date()
            except ValueError:
                birthdate = None

            try:
                first_appt_date = parser.parse(
                    date_first_appt).date().strftime("%x")
            except ValueError:
                first_appt_date = ""

            try:
                validate_international_phonenumber(phone)
            except ValidationError:
                phone = ""

            try:
                validate_international_phonenumber(other_phone)
            except ValidationError:
                other_phone = ""

            try:
                validate_email(email)
            except ValidationError:
                email = ""

            data = {
                "other_names": other_names,
                "other_phone": other_phone,
                "first_appointment_date": first_appt_date,
                "adult_dependant": adult_dependant,
                "address": address,
                "notes": notes,
                "next_of_kin": next_of_kin,
                "next_of_kin_relationship": next_of_kin_relationship,
                "next_of_kin_phone": next_of_kin_phone,
            }

            Client.objects.update_or_create(
                client_id=client_id,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "birth_date": birthdate,
                    "customer": customer,
                    "creator": creator,
                    "payment": Client.SELF_PAYING,
                    "data": data,
                })
