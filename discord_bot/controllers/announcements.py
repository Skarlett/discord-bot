from discord import Embed
from ..config import announcement
from ._bot import bot
from datetime import datetime


@bot.listen()
async def on_message(msg):
   ''' Listens for admin announcements '''
   if msg.channel.id == announcement.CopyChannelId:
     
     #TODO Add attachment for thumbnail
     
     embed = Embed(
       title=f"{msg.author}", description=msg.content,
       color=0xff0000, # thumbnail=announcement.ADMIN_THUMBNAIL
     )
     #embed.set_image("https://crafatar.com/avatars/")
     embed.set_author(name="Server Announcment")
     embed.set_footer(text=f"By {msg.author} | {datetime.now().strftime('%m/%d/%y %H:%M')}")
     
     
     channel = await bot.fetch_channel(announcement.CopyToId)
     
     await channel.send(embed=embed)
