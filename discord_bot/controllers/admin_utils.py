from discord.ext import commands
from ..utils import restrictive_check, uuid
from ._bot import bot


@bot.command()
@commands.guild_only()
@commands.check(restrictive_check)
async def purge(ctx):
  await ctx.channel.purge(limit=2000)

