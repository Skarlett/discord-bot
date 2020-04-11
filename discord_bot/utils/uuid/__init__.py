from .utils import is_mc_uuid
from .frame import API
import json

class Mojang(API):
  URL = "https://api.mojang.com/users/profiles/minecraft/{ctx}"
  @classmethod
  def parse(cls, payload):
    return json.loads(payload)['id']


class MinecraftAPI(API):
  URL = "https://minecraft-api.com/api/uuid/uuid.php?pseudo={ctx}"
  @classmethod
  def parse(cls, payload):
    return payload.strip()


class MineTools(API):
  URL = "https://api.minetools.eu/uuid/{ctx}"
  @classmethod
  def parse(cls, payload):
    return json.loads(payload)['id']


async def get_by_uuid(client, username, sources=(MineTools, Mojang, MinecraftAPI)):
  uuid = None
  for api in sources:
    uuid = await api.get_uuid(username, client)
    if uuid:
      break
  return uuid