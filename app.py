#!/usr/bin/env python3
######################
# Author: Adam Bortnik
# General usage bot -
# Refer to README.md for more documentation.
# NOTE: Assumes Linux based system.
######################
__author__  = "https://github.com/Skarlett"
__version__ = "0.2.0"
######################
from sys import version_info
from os import name as OSTYPE
import logging

if not(version_info[0] >= 3 and version_info[1] >= 7):
  if OSTYPE == 'posix':
    print("\033[1;31mUse python 3.7 or above.\033[0m")
  else:
    print("Use python 3.7 or above.")
  exit(1)

######################################################
# Logging
######################################################
from discord_bot.utils.loghandle import TimedGunzippedRotatingFileHandler as LogHandle
# This script will rotate its own logs,
########
# How many days to keep logs, +1 for today
# 0 - No backups besides today
LOGBACKUPS = 6
#######
# Directory to log to
LOGNAME = "./bugbot.log"
#######
# What to capture in logs
LOGLEVEL = logging.INFO

handler = LogHandle(
  LOGNAME,
  when='midnight',
  backupCount=6
)
handler.suffix = "%Y-%m-%d"

logging.basicConfig(
  # handlers=(handler,), # Allow GZIP Timed Handle to write to disk
  level=LOGLEVEL,
  format="%(asctime)s:%(levelname)s:%(message)s"
)
# import uvloop
import asyncio

from discord_bot.controllers import bot
from discord_bot.config import core
from discord_bot.controllers.http import setup, app

def main():
  #loop = uvloop.new_event_loop()
  #asyncio.set_event_loop(loop)
  loop = asyncio.get_event_loop()
  
  loop.create_task(setup(app))
  #web.run_app(app, reuse_port=True, port=8888)
  
  bot.run(core.TOKEN)
  #loop.run_forever()
if __name__ == '__main__':
  main()
  
