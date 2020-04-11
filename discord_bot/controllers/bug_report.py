import logging
from discord.ext import commands
from ._bot import bot
from ..config import bug_report
from ..utils.discord import create_dm_with_help, questionnaire, pagify, menu_pick_single
from ..utils import restrictive_check


@bot.command()
@commands.guild_only()
@commands.cooldown(3600, 3) # submit 3 bugs within the hour
@commands.check(restrictive_check)
async def bug(ctx):
  '''
  Report a bug/glitches
  '''
  report_to = await bot.fetch_channel(bug_report.ReportTo)
  
  if not report_to:
    await ctx.channel.send("We are currently not accepting bug reports")
    return

  dm_channel = await create_dm_with_help(ctx)
  
  if dm_channel:
    logging.info(f"{ctx.message.author} has began a bug transaction")
    await dm_channel.send(bug_report.MenuPreamble)
    
    category, questions = await menu_pick_single(
      dm_channel, ctx.author, bug_report.bug_menu,
      preamble="Plus use the options below to select the category you're reporting"
    )
    
    answers, files = await questionnaire(ctx, questions, dm_channel)
    await dm_channel.send(bug_report.DefaultEnding)
      
    for page in pagify(f"Bug report submitted by: **{ctx.author}** [**{category}**]\n"+'\n'.join(f'**{question}**: ```{answer.content}```' for question, answer in answers)):
      await report_to.send(page)
    
    if files:
      await report_to.send(files=files[:4])
  
  