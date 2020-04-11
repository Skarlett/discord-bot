import logging
from aiohttp import web
from ._base import app, routes
from . import mc2discord, announcements


async def setup(webapp, port=8888):
  webapp.add_routes(routes)
  runner = web.AppRunner(webapp)
  await runner.setup()
  #site = web.UnixSite(runner, '/tmp/bot-listener.sock')
  
  site = web.TCPSite(runner, host='0.0.0.0', port=port, reuse_address=True)
  logging.info(f"Running webserver API at http://0.0.0.0:{port}")
  await site.start()
  