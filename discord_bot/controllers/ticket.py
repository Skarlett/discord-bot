from ._bot import bot
from ..config import tickets
from ..utils import restrictive_check
from ..utils.discord import questionnaire, create_dm_with_help, add_options, FileOpts
from ..utils.discord.pager import ImagePaginator, EmptyPaginatorEmbed
from discord.ext import commands
from typing import List, Optional, Tuple
from discord import Embed, Member, Message, Reaction
from discord.ext.commands import Context, Paginator

import asyncio
import datetime
import logging


FIRST_EMOJI = "\u23EE"   # [:track_previous:]
LEFT_EMOJI = "\u2B05"    # [:arrow_left:]
RIGHT_EMOJI = "\u27A1"   # [:arrow_right:]
LAST_EMOJI = "\u23ED"    # [:track_next:]
DELETE_EMOJI = "\u274c"  # [:x:]


PAGINATION_EMOJI = [FIRST_EMOJI, LEFT_EMOJI, RIGHT_EMOJI, LAST_EMOJI, DELETE_EMOJI]

log = logging.getLogger(__name__)


class Permission:
  Senior = "@Senior"
  Mod = "@Moderator"


class StaticImagePaginator(Paginator):
    """
    Helper class that paginates images for embeds in messages persistently

    Close resemblance to LinePaginator, except focuses on images over text.

    Refer to ImagePaginator.paginate for documentation on how to use.
    """
  
    def __init__(self, prefix: str = "", suffix: str = ""):
      super().__init__(prefix, suffix)
      self._current_page = [prefix]
      self.images = []
      self._pages = []
  
    def add_line(self, line: str = '', *, empty: bool = False) -> None:
      """Adds a line to each page."""
      if line:
        self._count = len(line)
      else:
        self._count = 0
      self._current_page.append(line)
      self.close_page()
  
    def add_image(self, image: str = None) -> None:
      """Adds an image to a page."""
      self.images.append(image)
  
    @classmethod
    async def paginate(
        cls,
        pages: List[Tuple[str, str]],
        ctx: Context, embed: Embed,
        prefix: str = "",
        suffix: str = "",
        timeout: int = 300,
        exception_on_empty_embed: bool = False
    ) -> Optional[Message]:
      """
      Use a paginator and set of reactions to provide pagination over a set of title/image pairs.

      The reactions are used to switch page, or to finish with pagination.

      When used, this will send a message using `ctx.send()` and apply a set of reactions to it. These reactions may
      be used to change page, or to remove pagination from the message.

      Note: Pagination will be removed automatically if no reaction is added for five minutes (300 seconds).

      Example:
      >>> embed = Embed()
      >>> embed.set_author(name="Some Operation", url=url, icon_url=icon)
      >>> await ImagePaginator.paginate(pages, ctx, embed)
      """
    
      def check_event(reaction_: Reaction, member: Member) -> bool:
        """Checks each reaction added, if it matches our conditions pass the wait_for."""
        return all((
          # Reaction is on the same message sent
          reaction_.message.id == message.id,
          # The reaction is part of the navigation menu
          reaction_.emoji in PAGINATION_EMOJI,
          # The reactor is not a bot
          not member.bot
        ))
    
      paginator = cls(prefix=prefix, suffix=suffix)
      current_page = 0
    
      if not pages:
        if exception_on_empty_embed:
          log.exception(f"Pagination asked for empty image list")
          raise EmptyPaginatorEmbed("No images to paginate")
      
        log.debug("No images to add to paginator, adding '(no images to display)' message")
        pages.append(("(no images to display)", ""))
    
      for text, image_url in pages:
        paginator.add_line(text)
        paginator.add_image(image_url)
    
      embed.description = paginator.pages[current_page]
      image = paginator.images[current_page]
    
      if image:
        embed.set_image(url=image)
    
      if len(paginator.pages) <= 1:
        return await ctx.send(embed=embed)
    
      embed.set_footer(text=f"Page {current_page + 1}/{len(paginator.pages)}")
      message = await ctx.send(embed=embed)
    
      for emoji in PAGINATION_EMOJI:
        await message.add_reaction(emoji)
    
      while True:
        # Start waiting for reactions
        try:
          reaction, user = await ctx.bot.wait_for("reaction_add", timeout=timeout, check=check_event)
        except asyncio.TimeoutError:
          log.debug("Timed out waiting for a reaction")
          break  # We're done, no reactions for the last 5 minutes
      
        # Deletes the users reaction
        await message.remove_reaction(reaction.emoji, user)
      
        # Delete reaction press - [:x:]
        if reaction.emoji == DELETE_EMOJI:
          log.debug("Got delete reaction")
          break
      
        # First reaction press - [:track_previous:]
        if reaction.emoji == FIRST_EMOJI:
          if current_page == 0:
            log.debug("Got first page reaction, but we're on the first page - ignoring")
            continue
        
          current_page = 0
          reaction_type = "first"
      
        # Last reaction press - [:track_next:]
        if reaction.emoji == LAST_EMOJI:
          if current_page >= len(paginator.pages) - 1:
            log.debug("Got last page reaction, but we're on the last page - ignoring")
            continue
        
          current_page = len(paginator.pages - 1)
          reaction_type = "last"
      
        # Previous reaction press - [:arrow_left: ]
        if reaction.emoji == LEFT_EMOJI:
          if current_page <= 0:
            log.debug("Got previous page reaction, but we're on the first page - ignoring")
            continue
        
          current_page -= 1
          reaction_type = "previous"
      
        # Next reaction press - [:arrow_right:]
        if reaction.emoji == RIGHT_EMOJI:
          if current_page >= len(paginator.pages) - 1:
            log.debug("Got next page reaction, but we're on the last page - ignoring")
            continue
        
          current_page += 1
          reaction_type = "next"
      
        # Magic happens here, after page and reaction_type is set
        embed.description = ""
        await message.edit(embed=embed)
        embed.description = paginator.pages[current_page]
      
        image = paginator.images[current_page]
        if image:
          embed.set_image(url=image)
      
        embed.set_footer(text=f"Page {current_page + 1}/{len(paginator.pages)}")
        log.debug(f"Got {reaction_type} page reaction - changing to page {current_page + 1}/{len(paginator.pages)}")
      
        await message.edit(embed=embed)
    
      log.debug("Ending pagination and removing all reactions...")
      await message.clear_reactions()


def content(ctx):
  pkg = ctx.message.content.split(' ', 1)
  if len(pkg) > 1:
    return str(pkg[1])
  return 'None'
  
async def fill_ticket(msg, reviewee):
  channel = await bot.fetch_channel(tickets.TicketAudit)
  embed = msg.embeds[0]
  embed.color = 0x02FF00
  embed.set_footer(text=f"{reviewee} | Alive for {datetime.datetime.utcnow() - msg.created_at}")
  await channel.send(embed=embed)
  await msg.delete()


# https://github.com/Rapptz/discord.py/issues/2462
@bot.listen()
async def on_raw_reaction_add(payload):
  # Its too redundant to store ids in a db to check
  # this also ignores cache - so upon restarts will continue to work as expected
  if payload.channel_id == tickets.TicketChannel and bot.user.id != payload.user_id:

    channel = await bot.fetch_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    # guild = await bot.fetch_guild(payload.guild_id)

    reviewee = await bot.fetch_user(payload.user_id)

    #moderator = guild.get_role(tickets.TicketRole)
    #senior = guild.get_role(tickets.SeniorTicketRole)
    
    mods = [] # [x.id for x in moderator.members]
    admins = [] # [x.id for x in senior.members]
    
    mods.extend(tickets.Moderators)
    admins.extend(tickets.Seniors)
    
    permission = msg.embeds[0].fields[1].value

    if reviewee.id in mods:
      if permission == Permission.Mod:
        if payload.emoji == tickets.Raise:
          new_embed = msg.embed
          new_embed.color = 0xff0000
          new_embed.set_field_at(1, name="Ticket level", value=Permission.Senior)
          await msg.edit(embed=new_embed)
          await msg.clear_reactions()
          await add_options(msg, tickets.OkEmoji)
          return

        elif payload.emoji == tickets.OkEmoji:
          await fill_ticket(msg, reviewee)
          return

    elif reviewee.id in admins:
      # NOTE wont work with custom Emojis
      if ord(str(payload.emoji)) == ord(tickets.OkEmoji):
        await fill_ticket(msg, reviewee)
        return

    else:
      await msg.remove_reaction(payload.emoji, reviewee)

@bot.command()
@commands.check(restrictive_check)
@commands.cooldown(60*60*48, 1) # 48 hour cooldown
async def paymentissue(ctx):
  ''' Need help with a payment issue? '''
  embed = Embed(title=f"{ctx.message.author}", color=0xff0000)
  embed.add_field(name="Payment Issue", value=f"{content(ctx)}")
  embed.add_field(name="Ticket level", value=Permission.Senior, inline=True)
  
  dm_channel = await create_dm_with_help(ctx)
  
  if dm_channel:
    if tickets.PaymentPreamble:
      await dm_channel.send(tickets.PaymentPreamble.format(user=ctx.author.name))
    
    answers, files = await questionnaire(ctx, tickets.PaymentQuestions, channel=dm_channel, filesopt=FileOpts.URLs)

    NL = '\n'
    
    embed.add_field(
      name="Triage",
      value=f"{(NL + '-' * 30 + NL).join(f'**{q}**: {m.content}' for q, m in answers)}",
      inline=False
    )
    
    if tickets.DefaultEnding:
      await dm_channel.send(tickets.DefaultEnding)
    
    if answers:
      if len(files) > 1:
        await ImagePaginator.paginate(tuple(('.', f) for f in files), ctx, embed)
      elif len(files) == 1:
        embed.set_image(url=files[0])
      
      channel = await bot.fetch_channel(tickets.TicketChannel)
      msg = await channel.send(embed=embed)
      await add_options(msg, tickets.OkEmoji)
  
  
@bot.command()
@commands.check(restrictive_check)
#@commands.cooldown(3, 60*60*2) # 2 hour cooldown
async def mapissue(ctx):
  ''' Report something wrong with the Map '''
  embed = Embed(title=ctx.message.author.name, color=0xffD000)
  embed.add_field(name="Map Issue", value=f"{content(ctx)}")
  embed.add_field(name="Ticket level", value=Permission.Senior, inline=True)
  
  channel = await bot.fetch_channel(tickets.TicketChannel)
  msg = await channel.send(embed=embed)
  await add_options(msg, tickets.OkEmoji, tickets.Raise)


@bot.command()
#@commands.cooldown(3, 60 * 60 * 2)  # 2 hour cooldown
@commands.check(restrictive_check)
async def reportuser(ctx):
  embed = Embed(title=ctx.message.author.name, color=0xFFD000)
  embed.add_field(name="User Report", value=f"{content(ctx)}")
  embed.add_field(name="Ticket level", value=Permission.Mod, inline=True)
  
  channel = await bot.fetch_channel(tickets.TicketChannel)
  msg = await channel.send(embed=embed)
  await add_options(msg, tickets.OkEmoji, tickets.Raise)


@bot.command()
@commands.check(restrictive_check)
#@commands.cooldown(1, 60 * 60 * 2)  # 2 hour cooldown
async def requeststaff(ctx):
  embed = Embed(title=ctx.message.author.name, description=content(ctx), color=0xFFD000)
  embed.add_field(name="Support Request", value=f"{content(ctx)}")
  embed.add_field(name="Ticket level", value=Permission.Mod, inline=False)
  
  channel = await bot.fetch_channel(tickets.TicketChannel)
  msg = await channel.send(embed=embed)
  await add_options(msg, tickets.OkEmoji, tickets.Raise)


