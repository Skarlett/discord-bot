import base64
import logging

from aiohttp.web import Response
from aiohttp import ClientSession
from ._base import routes
from .._bot import bot
from ...config import mc2discord
from ..mc2discord import minecraft_registration
from ...models import DiscordUser, MinecraftUser, Session
from ...utils import uuid
#

@routes.post('/register')
async def register(request):
  '''
  {
    'mcname': str,
    'key': base64(bytes(32)),
    'cloud_key': base64(bytes(32))
  }

  warning: if a user discovers the key, and crafts an sql payload, then uses ssfr attack
  (key doesnt have to be discovered to use ssrf),
  or manages to bypass mitigation, it will result in an sql injection
  '''

  data = await request.post()

  for x in ('mcname', 'key', 'cloud_key'):
    if not x in data:
      return Response(status=405)

  if base64.urlsafe_b64decode(data['cloud_key']) != mc2discord.CLOUDKEY:
    logging.warning("FALSE CLOUD-API KEY FROM {}".format(request.hdr))
    return Response(status=403)

  pkg = minecraft_registration[data['mcname']]  # dict['minecraft_name'] = (time.time(), discord_id, key)

  _, discord_id, key = pkg
  user = await bot.fetch_user(discord_id)

  if not user:
    return Response(status=500)

  if not key == base64.urlsafe_b64decode(data['key']):
    return Response(status=405)
  
  async with ClientSession() as client:
    mc_uuid = await uuid.get_by_uuid(client, data['mcname'])
  
  #return Response(status=200, text="OK")

  if not mc_uuid:
    return Response(status=500)

  db = Session()

  if db.query(MinecraftUser).get(mc_uuid):
    return Response(status=405)

  user = db.query(DiscordUser).get(discord_id)
  if not user:
    parent = DiscordUser(uuid=discord_id)
    db.add(parent)
  else:
    parent = db.query(DiscordUser).get(discord_id)

  mcacc = MinecraftUser(uuid=mc_uuid.replace('-', ''), discord=parent)
  db.add(mcacc)

  db.commit()
  db.flush()

  # try:
  #   channel = await user.create_dm()
  #   await channel.send('Registered! :thumbsup:')
  # except Forbidden:
  #   pass

  logging.info(f"Registered {mc_uuid} to {discord_id}")
  return Response(text="OK")
