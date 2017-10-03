"""
"Labels" allow us the flexibility of have different names for everything
defined here
 e.g. in one set up a "Doctor" may be known as a "Lawyer"
"""

from django.utils.translation import ugettext as _

APPOINTMENT = _("Appointment")
CREATE_APPOINTMENT = _("Add Appointment")

CLIENT = _("Client")
CLIENT_PLURAL = _("Clients")
SELECT_CLIENT = _("Select Client")
CREATE_CLIENT = _("Create New Client")
EDIT_CLIENT = _("Edit Client")
CLIENT_ID = _("Client ID")

DOCTOR_TITLE = _("")
DOCTOR = _("Doctor")
DOCTOR_PLURAL = _("Doctors")

ASSISTANT = _("Assistant")
ASSISTANT_PLURAL = _("Assistants")

VENUE = _("Schedule")
VENUE_PLURAL = _("Schedules")
VIEW = _("View")
VIEW_PLURAL = _("Views")

DESCRIPTION = _("Notes")

OPENING_HOUR = _("Opening Hour")
OPENING_HOUR_PLURAL = _("Opening Hours")
