#!/usr/bin/env python
import requests
import sys
import base64

CLOUDKEY = b'vo$F|\xbeo\xc1\x10#\x98\xac\x8f\xd6P\xfa #\x1c\xd0\xb0g\xe9U\x1e\xf0(\xa3\x89f3\xb4'
SERVER = "http://127.0.0.1:8888/register"


if not len(sys.argv) == 2:
  print(f"./{sys.argv[0]} <username> <transaction-uuid>")


data = {
  'key': sys.argv[2].strip(),
  'mcname': sys.argv[1].strip(),
  'cloud_key': base64.b64encode(CLOUDKEY)
}

resp = requests.post(SERVER, data=data)
if resp.ok:
  print('OK')
else:
  print(resp.status_code)
