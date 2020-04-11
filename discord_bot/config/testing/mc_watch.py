timeout = 15
CheckEvery = 60

###
# Notify someone if service hasn't responded in X seconds
NotifyAfter = 60
NotifyStaff = True

# Roles to meantion
NotifyRoles = ()

#  staff ChannelID
NotifyAt = 665031593227714617

# dev.jdc.media 167.172.124.45:22:80
# stats.jdc.media 206.189.164.175:22:80
# jdc.media 198.27.68.30:22:80


ChannelToMinecraft = [
  # Use public IPs so we know we're routable.
  #ID                   OK                 Offline           IP              PORT
  (665032127330648074, ("✅http", "🚫http"), ("198.27.68.30", 80)),
  (655400180606042122, ("✅ssh", "🚫ssh"), ("198.27.68.30", 22)),
  
  (664948723276578816, ("✅http", "🚫http"), ("167.172.124.45", 80)),
  (664948755858194449, ("✅ssh", "🚫ssh"), ("167.172.124.45", 22)),
  
  (664949072821485610, ("✅http", "🚫http"), ("206.189.164.175", 80)),
  (664949088621559826, ("✅ssh", "🚫ssh"), ("206.189.164.175", 22)),
]


