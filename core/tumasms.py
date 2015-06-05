#!/usr/bin/python

"""This module implements a python connector for the tumasms SMS api
"""
__all__ = ['Tumasms']

from copy import copy
import xml.etree.ElementTree as ET
import urllib
import urllib2
import json


API_URL = "http://tumasms.co.ke/ts/api/"
API_SEND_PATH = "send_sms"
API_GET_PATH = "get_balance"
SMS_XML_TEMPLATE = "<sms><recipient>%s</recipient><message>%s</message><sender>%s</sender><scheduled_date>%s</scheduled_date></sms>"
MESSAGES_TEMPLATE = "<request>%s</request>"


def to_dict(et):
    """Convert Etree to dictionary
    Values picked from node text - keys from tags.
    """
    result = {}
    for item in et:
        if item.text:
            result[item.tag] = item.text
        else:
            result[item.tag] = to_dict(item)
    return result


class Tumasms(object):

    def __init__(self, api_key, api_signature, api_parameters={}, sms_messages=[]):
        """Initialize connector instance.
        """
        self.api_parameters = api_parameters
        self.api_parameters.update(
            dict(api_key=api_key, api_signature=api_signature)
        )
        self.sms_messages = sms_messages
        self.response = None
        self.status = None

    def queue_sms(self, recipient, message, sender="", scheduled_date=""):
        """Add an sms to list of messages to send"""
        self.sms_messages.append(SMS_XML_TEMPLATE % (recipient, message, sender, scheduled_date))

    def _get_messages(self):
        return MESSAGES_TEMPLATE % "".join(self.sms_messages)

    def send_sms(self):
        """Build messages into parameters for a send operation
        """
        self.execute({"messages": self._get_messages()})

    def get_balance(self):
        """Get available text messages
        """
        self.execute({}, action=API_GET_PATH)

    def status(self):
        if self.response:
            return self.response_dict["status"]["type"]

    def message(self):
        if self.response:
            return int(self.response_dict["content"]["messages"]["message"])

    def description(self):
        if self.response:
            return self.response_dict["description"]

    def execute(self, params, action=API_SEND_PATH):
        """Send HTTP POST to action url with encoded paramters
        """

        # include api parameters in request (always a POST)
        params.update(self.api_parameters)
        _url = "%s%s" % (API_URL, action)
        request = urllib2.Request(_url, urllib.urlencode(params))
        self.response = urllib2.urlopen(request).read()
        self.response_xml = self.response
        _etree = ET.fromstring(self.response)
        self.response_dict = to_dict(_etree)
        self.response_json = json.dumps(self.response_dict)
