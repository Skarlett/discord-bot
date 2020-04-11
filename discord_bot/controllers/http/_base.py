from aiohttp import web

app = web.Application()

routes = web.RouteTableDef()

@routes.get('/test')
async def hello(req):
  return web.Response(text="Hello")


@routes.get('/')
async def index(req):
  return web.Response(text="Index")