#!/usr/bin/env python
from tacacs_plus.client import TACACSClient
from tacacs_plus.flags import TAC_PLUS_ACCT_FLAG_START, TAC_PLUS_ACCT_FLAG_WATCHDOG, TAC_PLUS_ACCT_FLAG_STOP
from properties.properties import LoginProps
import socket

def request_auth(user, password):
  """ Request authentication login against ClearPass server via TACACS+"""

  # Connection with Clearpass Server via Tacacs+
  cli = TACACSClient(LoginProps.CLEARPASS_IP, 49, LoginProps.CLEARPASS_SECRET, timeout=10, family=socket.AF_INET)
  print("cli = ", cli)
  # authenticate user and password
  authen = cli.authenticate(user, password)
  print("authen = ", authen)
  # Handle the response code
  if (authen.valid):
    return 200
  else:
    return 401