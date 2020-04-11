import logging


class API:
  URL = None
  METHOD = "get"
  
  @classmethod
  def parse(cls, payload):
    return None
  
  @classmethod
  async def fetch(cls, data, engine):
    assert cls.URL
    try:
      logging.info(f"[{super().__name__}] Sending HTTP request")
      resp = await getattr(engine, cls.METHOD)(cls.URL.format(ctx=data))
      data = await resp.text()
      return cls.parse(data.replace('-', '').strip())
    except Exception as e:
      logging.exception(e)
      return None