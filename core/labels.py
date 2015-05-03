"""
"Labels" allow us the flexibility of have different names for everything defined here
 e.g. in one set up a "Doctor" may be known as a "Lawyer"
"""

from django.utils.translation import ugettext as _

APPOINTMENT = _("Appointment")

CLIENT = _("Patient")
CLIENT_PLURAL = _("Patients")
SELECT_CLIENT = _("Select Patient")
CREATE_CLIENT = _("Create New Patient")
CLIENT_ID = _("File Number")

DOCTOR_TITLE = _("Dr.")
DOCTOR = _("Doctor")
DOCTOR_PLURAL = _("Doctors")

VENUE = _("Clinic")
VENUE_PLURAL = _("Clinics")

DESCRIPTION = _("Treatment")
