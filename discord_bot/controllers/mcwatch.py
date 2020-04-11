from discord import Embed
from ..config import  mc_watch
from ..utils import htime
from ._bot import bg_task, bot

import asyncio
import datetime
import time
import logging


def ascii(s):
  return ''.join([c for c in s if ord(c) < 128])


async def check_service(target, port, timeout=mc_watch.timeout):
  try:
    #TODO Close stream
    _ = await asyncio.wait_for(asyncio.open_connection(target, port=port), timeout=timeout)
    #print(rx, tx)
    #tx.close()
    #rx.close()
  except (asyncio.TimeoutError, ConnectionRefusedError) as e:
    return False
  return True

notified = {} # {channel_id:int: (downtime:int, msg:Message) }

async def check_if_still_dead(addr, status, channel):
  await asyncio.sleep(mc_watch.NotifyAfter)
  if not await check_service(*addr):
    logging.warning(f"{addr[0]}:{addr[1]} Still down after {mc_watch.NotifyAfter} seconds, notifying staff.")
    
    send_to = await bot.fetch_channel(mc_watch.NotifyAt)
    embed = Embed(title=f"{ascii(channel.name).strip('-')}", color=0xff0000)
    
    #TODO Check
    embed.set_footer(text=' '.join([
      role.mention for role in channel.guild.roles
      if role.id in mc_watch.NotifyRoles and role.mentionable
    ]))
    
    embed.add_field(name=f"Service Down - {ascii(channel.name).strip('-')}", value=f"Downed at {datetime.datetime.now()}")
    msg = await send_to.send(embed=embed)
    notified[channel.id] = (notified[channel.id][0], msg)
    return
  await channel.edit(name=status[0])

async def correct_notification(channel_id):
  downtime, msg = notified[channel_id]
  if msg:
    embed = msg.embeds[0]
    ht = htime(time.time(), downtime)
    embed.set_footer(text=f"Issue Resolved in: {ht}")
    embed.color = 0x0FFF00
    await msg.edit(embed=embed)

# @bg_task(wait=mc_watch.CheckEvery)
# async def check_mc_services():
#   for channel_id, channel_status, addr in mc_watch.ChannelToMinecraft:
#     channel = await bot.fetch_channel(channel_id)
#
#     logging.debug(f"Checking {addr}")
#     if await check_service(*addr):
#       # Passed
#       if channel.id in notified:
#         logging.debug(f"{addr} Back online.")
#         await correct_notification(channel.id)
#         notified.pop(channel.id)
#
#       await channel.edit(name=channel_status[0])
#
#     else:
#       # Failed
#       logging.warning(f"{addr[0]}:{addr[1]} Went down.")
#       await channel.edit(name=channel_status[1])
#       if not channel.id in notified and mc_watch.NotifyStaff:
#         notified[channel.id] = (time.time(), None)
#         asyncio.create_task(check_if_still_dead(addr, channel_status, channel))
