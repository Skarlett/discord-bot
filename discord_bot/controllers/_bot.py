import logging
import asyncio

from discord.ext import commands
from ..config import core
from ..utils import parametrized_decorator

bot = commands.Bot(core.PREFIX)

@bot.listen()
async def on_ready():
  logging.info("{} Online".format(bot.user.name))
  
@parametrized_decorator
def bg_task(fut, wait=30, bot_ready=True):
  async def wrapper(*args, **kwargs):
    while True:
        if bot_ready:
          await bot.wait_until_ready()
        await fut(*args, **kwargs)
        await asyncio.sleep(wait)
  bot.loop.create_task(wrapper())
  return fut
