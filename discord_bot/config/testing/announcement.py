
######################################################
# HTTP Listener
######################################################
PORT = 8888


ZAPIERKEY = b'\x04s&\xecJQ5q\tA1\xf5\x99\xfe\xeb8\x00\xf2\xfb\x02\xf6:a\xd4Yf\xdd\xd8\xba\x88l\xf3'
# BHMm7EpRNXEJQTH1mf7rOADy+wL2OmHUWWbd2LqIbPM=
# use `base64.urlsafe_b64encode(ZAPIERKEY)` when inputting into zapier
# python discord_bot/config/<config>/announcement.py -i

######################################################
# Announcement configurations
######################################################
CopyChannelId = 655400784695132170
CopyToId      = 655400397112082463

ADMIN_COLOR = 0xFF7400
ADMIN_THUMBNAIL = ""
ADMIN_CHANNEL = 646038135968366623
######################################################
# Commit Message
######################################################
# `repo`, `branch`, `hash`, `author`, `message`
# are all variables you can use
COMMIT_NAME    = "⚙ **Updates made to {repo}/{branch}**"
COMMIT_BODY    = "{message}"
COMMIT_FOOTER  = "⚙ Powered by {author}"
COMMIT_COLOR   = 0x06a800
COMMIT_THUMBNAIL = "https://www.kaspersky.com/content/en-global/images/icons/compare-table/icon-software-updates.png"
# Dont announce in the community
COMMIT_CHANNEL = 646038700647645204
PRIVATE_COMMIT_PREFIX = "private-commit"

######################################################
# Youtube
######################################################
YT_COLOR = 0xFF0000
YT_THUMBNAIL = "https://seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png"
YT_CHANNEL = 646038823683227668
######################################################
# Twitter
######################################################
TWITTER_COLOR = 0x00C3FF
TWITTER_THUMBNAIL = "https://sdweg.files.wordpress.com/2016/09/l62697-new-twitter-logo-49466.png"
TWITTER_CHANNEL = 646038966281306112
