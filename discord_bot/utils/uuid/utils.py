from string import hexdigits



def is_mc_uuid(data):
  if len(data) == 32:
    for x in data:
      if not x in hexdigits:
        return False
    return True
  return False
