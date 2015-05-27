"""
"Labels" allow us the flexibility of have different names for everything defined here
 e.g. in one set up a "Doctor" may be known as a "Lawyer"
"""

from django.utils.translation import ugettext as _

APPOINTMENT = _("Appointment")
CREATE_APPOINTMENT = _("Add Appointment")

CLIENT = _("Patient")
CLIENT_PLURAL = _("Patients")
SELECT_CLIENT = _("Select Patient")
CREATE_CLIENT = _("Create New Patient")
EDIT_CLIENT = _("Edit Patient")
CLIENT_ID = _("File Number")

DOCTOR_TITLE = _("Dr.")
DOCTOR = _("Doctor")
DOCTOR_PLURAL = _("Doctors")

ASSISTANT = _("Nurse")
ASSISTANT_PLURAL = _("Nurses")

VENUE = _("Clinic")
VENUE_PLURAL = _("Clinics")

DESCRIPTION = _("Treatment")

OPENING_HOUR = _("Opening Hour")
OPENING_HOUR_PLURAL = _("Opening Hours")
