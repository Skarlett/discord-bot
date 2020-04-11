from .mc2discord import DiscordUser, MinecraftUser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ._base import Base

engine = create_engine('sqlite:///bot.db', echo=True)

Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(bind=engine)

