import base64

from discord import Embed
from aiohttp.web import Response
from datetime import datetime
from ...config import announcement
from .._bot import bot
from ._base import routes


@routes.post('/commit')
async def commit(request):
  new = await request.post()['push'][0]['changes'][0]['new']
  
  passover = {
    'author': new['target']['author'],
    'message': new['target']['message'].strip(),
    'branch': new['name'],
    'repo': new['respository'],
    'hash': new['target']['hash']
  }
  
  # https://cog-creators.github.io/discord-embed-sandbox/
  embed = Embed(color=announcement.COMMIT_COLOR)
  embed.set_thumbnail(url=announcement.COMMIT_THUMBNAIL)
  embed.add_field(
    name=announcement.COMMIT_NAME.format(**passover),
    value=announcement.COMMIT_BODY.format(**passover),
    inline=True
  )
  embed.set_footer(text=announcement.COMMIT_FOOTER.format(**passover))
  
  if not announcement.PRIVATE_COMMIT_PREFIX in passover['message'].strip():
    channel = await bot.fetch_channel(announcement.COMMIT_CHANNEL)
    await channel.send(embed=embed)

@routes.post('/yt')
async def youtube(request):
  '''
  {'key',
  'title',
  'url',}
  '''
  data = await request.post()
  if 'key' in data and base64.urlsafe_b64decode(data['key']) == announcement.ZAPIERKEY:
    embed = Embed(color=announcement.YT_COLOR)
    embed.set_thumbnail(url=announcement.YT_THUMBNAIL)
    embed.add_field(
      name=data['title'],
      value=data['url'],
      inline=True
    )
    
    channel = await bot.fetch_channel(announcement.YT_CHANNEL)
    await channel.send(embed=embed)
  return Response(status=200)

@routes.post('/twitter')
async def twitter(request):
  '''
      {'key',
      'text',
      'url',}
      '''
  
  data = await request.post()
  if 'key' in data and base64.urlsafe_b64decode(data['key']) == announcement.ZAPIERKEY:
    embed = Embed(color=announcement.YT_COLOR)
    embed.set_thumbnail(url=announcement.TWITTER_THUMBNAIL)
    embed.add_field(name="Chirp chirp!",
                    value=data['text'],
                    inline=True)
    
    embed.set_footer(text=f"Tweeted at {datetime.now()}")
    
    channel = await bot.fetch_channel(announcement.TWITTER_CHANNEL)
    await channel.send(embed=embed)
  return Response(status=200)
