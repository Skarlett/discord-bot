from ..config import core


restrictive_check = lambda ctx: not core.restrictive_usage or ctx.channel.id in core.bot_channels


def parametrized_decorator(decorator):
  def wraps(*args, **kwargs):
    def repl(function):
      return decorator(function, *args, **kwargs)
    return repl
  return wraps


def htime(end, start):
  hours, rem = divmod(end - start, 3600)
  minutes, seconds = divmod(rem, 60)
  return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def ascii(s):
  return ''.join([c for c in s if ord(c) < 128])



