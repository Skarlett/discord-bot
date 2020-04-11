from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from ._base import Base

import time
######################
# one-to-many setup  #
######################

class DiscordUser(Base):
  __tablename__ = 'discorduser'
  uuid = Column(Integer, primary_key=True)
  registered_at = Column(DateTime, default=datetime.now(), nullable=False)
  
  accounts = relationship(
    "MinecraftUser",
    backref=backref(
      "discord",
      cascade="all, delete-orphan",
      single_parent=True
    ),
  )


class MinecraftUser(Base):
  __tablename__ = 'minecraftuser'
  uuid = Column(String(32), primary_key=True)
  discord_id = Column(Integer, ForeignKey('discorduser.uuid'), nullable=False)
  registered_at = Column(DateTime, default=datetime.now(), nullable=True)
  