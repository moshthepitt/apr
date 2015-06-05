#!/usr/bin/python

# Load API Class
from tumasms import Tumasms

# Setup API credentials
API_SIGNATURE = "Your API Signature"  # Check under Settings->API Key in Tumasms
API_KEY = "Your API Key"  # Check under Settings->API key in Tumasms

# API Call to Send Message(s)
# Request
tumasms = Tumasms(API_KEY, API_SIGNATURE)  # Instantiate API library
# Replace example with valid recipient, message, sender id and scheduled
# datetime if required in format ("YYYY-MM-DD HH:mm:ss")Replace 0723XXXXXX
# with recipient and "Message 1." with your message
tumasms.queue_sms("+254723XXXXXX", "Message 1", "Sender_ID", "")
# Replace example with valid recipient, message, sender id and scheduled
# datetime if required in format ("YYYY-MM-DD HH:mm:ss")
tumasms.queue_sms("+254733XXXXXX", "Message 2", "Sender_ID", "")
tumasms.send_sms()  # Initiate API call to send messages
# Response
print tumasms.status  # View status either (SUCCESS or FAIL)
print tumasms.message  # Returns SMS available (Credits balance)
print tumasms.description  # Returns a status message
print tumasms.response_xml  # Returns full xml response
print tumasms.response_dict  # Returns xml response as a dictionary
print tumasms.response_json  # Returns full json response

# API Call to Check for Available SMS
# Request
tumasms = Tumasms(API_KEY, API_SIGNATURE)  # Instantiate API library
tumasms.get_balance()  # Initiate API call to check available messages
# Response
print tumasms.status  # View status either (SUCCESS or FAIL)
print tumasms.message  # Returns SMS available (Credits balance)
print tumasms.description  # Returns a status message
print tumasms.response_xml  # Returns full xml response
print tumasms.response_dict  # Returns xml response as a dictionary
print tumasms.response_json  # Returns full json response
