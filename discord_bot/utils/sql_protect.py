from . import ascii
import re

_sanitizer = re.compile(r"(!|@|#|\$|%|\^|&|\*|\(|\)|{|\}|-|\+|_|=|;|\'|\"|:|\||\\|\.|,|`|~)", re.MULTILINE)

def sanitize(txt):
  return _sanitizer.sub(ascii(txt), '')