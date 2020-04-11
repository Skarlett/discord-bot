from ...controllers._bot import bot
from ...config import core, util
from discord import Forbidden, File, Embed
from io import BytesIO

import aiohttp
import asyncio
import logging


def escape(text: str, *, mass_mentions: bool = False, formatting: bool = False) -> str:
  """Get text with all mass mentions or markdown escaped.
  Parameters
  ----------
  text : str
      The text to be escaped.
  mass_mentions : `bool`, optional
      Set to :code:`True` to escape mass mentions in the text.
  formatting : `bool`, optional
      Set to :code:`True` to escpae any markdown formatting in the text.
  Returns
  -------
  str
      The escaped text.
  """
  if mass_mentions:
    text = text.replace("@everyone", "@\u200beveryone")
    text = text.replace("@here", "@\u200bhere")
  if formatting:
    text = text.replace("`", "\\`").replace("*", "\\*").replace("_", "\\_").replace("~", "\\~")
  return text


def pagify(
    text: str,
    delims=["\n"],
    *,
    priority: bool = False,
    escape_mass_mentions: bool = True,
    shorten_by: int = 8,
    page_length: int = 2000):
  """Generate multiple pages from the given text.
  Note
  ----
  This does not respect code blocks or inline code.
  Parameters
  ----------
  text : str
      The content to pagify and send.
  delims : `sequence` of `str`, optional
      Characters where page breaks will occur. If no delimiters are found
      in a page, the page will break after ``page_length`` characters.
      By default this only contains the newline.
  Other Parameters
  ----------------
  priority : `bool`
      Set to :code:`True` to choose the page break delimiter based on the
      order of ``delims``. Otherwise, the page will always break at the
      last possible delimiter.
  escape_mass_mentions : `bool`
      If :code:`True`, any mass mentions (here or everyone) will be
      silenced.
  shorten_by : `int`
      How much to shorten each page by. Defaults to 8.
  page_length : `int`
      The maximum length of each page. Defaults to 2000.
  Yields
  ------
  `str`
      Pages of the given text.
  """
  in_text = text
  page_length -= shorten_by
  while len(in_text) > page_length:
    this_page_len = page_length
    if escape_mass_mentions:
      this_page_len -= in_text.count("@here", 0, page_length) + in_text.count(
        "@everyone", 0, page_length
      )
    closest_delim = (in_text.rfind(d, 1, this_page_len) for d in delims)
    if priority:
      closest_delim = next((x for x in closest_delim if x > 0), -1)
    else:
      closest_delim = max(closest_delim)
    closest_delim = closest_delim if closest_delim != -1 else this_page_len
    if escape_mass_mentions:
      to_send = escape(in_text[:closest_delim], mass_mentions=True)
    else:
      to_send = in_text[:closest_delim]
    if len(to_send.strip()) > 0:
      yield to_send
    in_text = in_text[closest_delim:]
  
  if len(in_text.strip()) > 0:
    if escape_mass_mentions:
      yield escape(in_text, mass_mentions=True)
    else:
      yield in_text


async def create_dm_with_help(ctx):
  try:
    channel = await ctx.author.create_dm()
    msg = await channel.send("testing...")
    await msg.delete()
    return channel
  except Forbidden:
    await ctx.channel.send(
      "Please allow direct messages sent from this server. "
      "Follow these instructions and retry in a minute!\n"
      "In the top left of the guild press the arrow\n"
      "https://raw.githubusercontent.com/Skarlett/_test/master/show_settings.png\n"
      "https://raw.githubusercontent.com/Skarlett/_test/master/server_settings.png\n"
      "https://raw.githubusercontent.com/Skarlett/_test/master/privacy_prompt.png", delete_after=90
    )
    await ctx.channel.send("Make sure this is turn on and try again.", delete_after=90)
    return None


class FileOpts:
  DiscordFiles = 1
  URLs = 2
  RawFd = 3


async def get_uploads(msg, fileopt):
  if msg.attachments:
    uploads = []
    for attachment in msg.attachments:
      async with aiohttp.ClientSession() as session:
        try:
          resp = await session.get(attachment.url)
          if fileopt == FileOpts.DiscordFiles:
            fd = File(BytesIO(await resp.content.read()), filename=attachment.url.split('/')[-1])
          elif fileopt == FileOpts.RawFd:
            fd = BytesIO(await resp.content.read())
          else:
            fd = attachment.url
          
          uploads.append(fd)
        
        except Exception as e:
          logging.critical("unhandled exception")
          logging.exception(e)
          continue
    return uploads
  return None


async def questionnaire(ctx, questions, channel=None, filesopt=FileOpts.DiscordFiles):
  answers = []
  files = []
  
  dm_channel = channel or await create_dm_with_help(ctx)
  if not dm_channel:
    return
  
  await dm_channel.send(util.QuestionnairePreamble)
  for question in questions:
    await dm_channel.send(question)
    try:
      msg = await bot.wait_for('message', check=lambda nctx: nctx.channel == dm_channel and ctx.author == nctx.author,
                               timeout=300.0)
    except asyncio.TimeoutError:
      await dm_channel.send("Timed out. Report discarded.")
      logging.warning('{}\'s Request timed out'.format(ctx.author))
      return
    except Exception as e:
      logging.exception(e)
      return
    
    if not msg.content and msg.attachments:
      msg.content = "<Uploaded Content>"
      files.extend(await get_uploads(msg, filesopt))
    
    if msg.content.startswith(core.PREFIX):
      cmd = msg.content[len(core.PREFIX):].lower().strip()
      if cmd == "restart":
        await ctx.reinvoke()
      elif cmd == "discard":
        return
    
    answers.append((question, msg))
  return answers, files


async def add_options(msg, *opts):
  for name in opts:
    await msg.add_reaction(name)


async def menu_pick_single(send_channel, author, menu, timeout=60, preamble_name="`Welcome`\n", preamble=""):
  embed = Embed(color=0x00FF13)
  
  if preamble_name and preamble:
    embed.add_field(name=preamble_name, value=preamble, inline=False)
  
  for emoji, item in menu.items():
    name, _ = item
    # menu_text += f'{emoji} - {name}\n'
    embed.add_field(name=name, value=emoji, inline=True)
  
  msg = await send_channel.send(embed=embed, delete_after=timeout)
  await add_options(msg, *menu.keys())
  
  try:
    
    react, user = await bot.wait_for('reaction_add', check=lambda r, u: u == author, timeout=timeout)
    return menu[str(react.emoji).strip()]
  
  except asyncio.TimeoutError:
    logging.warning(f"[{author}] Bug transaction timed out.")
    await send_channel.send("Request timed out.", delete_after=30)
