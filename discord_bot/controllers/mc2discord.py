import os
import time
import base64
import datetime
import aiohttp

from discord.ext import commands
from discord.utils import get
from ..config import mc2discord
from ._bot import bot, bg_task
from ..utils import restrictive_check, uuid, sql_protect
from ..models import MinecraftUser, DiscordUser, Session

minecraft_registration = dict() # dict['minecraft_name'] = (time.time(), discord_id, key)

@bg_task(wait=360)
async def check_regs_timeouts():
  remove = set()
  for k, v in minecraft_registration.items():
    if time.time() >= v[0] + mc2discord.MC_timeout:
      remove.add(k)
  
  for k in remove:
    minecraft_registration.pop(k)


@bot.command()
@commands.guild_only()
@commands.cooldown(1, 720)
@commands.check(restrictive_check)
async def register(ctx):
  '''
  Register your Minecraft accounts onto our discord.
  '''
  
  pkg = ctx.message.content.strip().split(" ")
  if len(pkg) == 2:
    mcname = pkg[1]

    async with aiohttp.ClientSession() as session:
      user_uuid = await uuid.get_by_uuid(session, mcname.strip())
      await session.close()
    
    db = Session()
    
    mcacc = db.query(MinecraftUser).get(sql_protect.sanitize(user_uuid))
    
    if not mcacc:
      key = os.urandom(mc2discord.USER_KEY_LEN)
      user_key = base64.urlsafe_b64encode(key)
      
      minecraft_registration[mcname] = (time.time(), ctx.message.author.id, key)
      
      await ctx.channel.send(
        'In-game at the top right corner of the main menu, press the :gear: icon and go to \"Register to Discord\" and insert  `{}` '\
        'complete registration within **{}**'
          .format(user_key.decode('utf-8'), str(datetime.timedelta(seconds=mc2discord.MC_timeout)))
      )
    else:
      await ctx.channel.send("Account already Registered")
  else:
    await ctx.channel.send('{} <minecraft username/uuid>')
  
@bot.command()
@commands.guild_only()
@commands.cooldown(1, 10)
async def mcuuid(ctx):
  ''' Looks up Minecraft user's UUID '''
  user = ctx.message.content.split(' ')[1]
  async with aiohttp.ClientSession() as session:
    user_uuid = await uuid.get_by_uuid(session, user)
    await session.close()
  
  if user_uuid:
    await ctx.channel.send(f'`{user_uuid}`')
  else:
    await ctx.channel.send("`Not found.`")

# @bot.command()
@commands.guild_only()
@commands.cooldown(1, 10)
async def stats(ctx):
  pass

# @bot.command()
@commands.guild_only()
@commands.cooldown(1, 10)
async def lookup(ctx):
  ''' Looks up Registered users '''

  session = Session()
  pkg = ctx.message.content.split(' ')

  if len(pkg) != 2:
    await ctx.message.send("Only one lookup at a time")
    return

  raw_user = pkg[1]
  discord_user = None
  mc_accounts = []

  if raw_user.isdigits():
    discord_user = session.query(DiscordUser).get(sql_protect.sanitize(raw_user).strip())

  elif ctx.message.mentions and not ctx.message.mention_everyone:
    if len(ctx.message.mentions[0]) > 1:
      await ctx.message.send("Only one lookup at a time")
      return

    user = ctx.message.mentions[0]
    discord_user = session.query(DiscordUser).get(user.id)

  elif uuid.is_mc_uuid(raw_user):
    user = session.query(MinecraftUser).get(sql_protect.sanitize(raw_user.replace('-', '')).strip())
    discord_user = session.query(DiscordUser).get(user.id)

  else: # ambiguous input
    
    # Discord username?
    users = get(bot.get_all_members(), name=raw_user)
    if users:
      available_users = session.query(DiscordUser).filter(lambda duser: duser.c.id in users)
      
      discord_user = session.query(DiscordUser).get(user.id)
    
    else:
      # Minecraft username?
      async with aiohttp.ClientSession() as session:
        #user_uuid = await uuid.get_by_name(session, raw_user)
  
        # if user_uuid:
        #   user = session.query(MinecraftUser).get(sql_protect.sanitize(user_uuid.replace('-', '')).strip())
  
        await session.close()
  
      if raw_user:
        pass


  async with aiohttp.ClientSession() as session:
    user_uuid = await uuid.get_mc_uuid(session, user)
    await session.close()

  if user_uuid:
    await ctx.channel.send(f'`{user_uuid}`')
  else:
    await ctx.channel.send("`Not found.`")