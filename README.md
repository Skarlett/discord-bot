# Discord [IN Testing]

This repository is a list of tools and capabilities.

NOTE: Local linking does not work on BitBucket.

## Main Feature list

| Feature          | Done  |
|:---------------- |:----- |
| [commit publicity](#commits) | ✅ |
| [Ingame name to discord](#Ingame2Discord) | ✅ |
| [Announcements](#Announcements) | ✅ |
| [Ticket System](#ticketing)    |  ✅ |
| [ServerStatus](#ServerStatus)  | ✅ |
| [Bug reporting](#bugreporting) | ✅ |

### Tech Details
### Core
Async engine (asyncio),
Async HTTP service (aiohttp.Web),
Sql Database + Framework (sqlalchemy),
Discord (discord.py),

### McWatch
Actively listens for services going down, after notifying staff, it will change the notification on resolve
While at the same time displaying the server status using Channel Names

### Misc add-ons
+ Pagify for questionnaires
+ Supports actions based on emojis
+ Supports mc-UUID lookup functions
+ Uses state of the art framework designs
+ Extensive Logging + Gunzipped + Logrotate timed
+ Automatic time-outs
+ Help menus

## Discord-bot
Implements the following

  - Public Commits
  - Announcements
  - Ticketing system
  - Server status
  - Bug reporting
  - Async HTTP Listener
  - Linking Ingame via MC-Plugin & HTTP Listener


# Setting up webhooks

### /register
#### POST
API EndPoint for cloud to comfirm Discord user registrations

### /commit
#### POST
https://confluence.atlassian.com/bitbucket/manage-webhooks-735643732.html

Mark only push, then using this Box's IP/Domain fill out `http://1.1.1.1/commit`

### /twitter
#### POST
Make an account at https://zapier.com/, -> make app

in step 2) Choose webhook, and paste in

You may format your Announcement message like such

for example - your key is `body` and you've selected `my tweets: Text`
then using `{body}` in the text message, you will recieve the value (The message's text we tweeted)

`"I made a tweet today: {body}\n{url}"`

these configurations can be made in `discord-bot/src/lib/settings.py`

### /yt
#### POST
Make an account at https://zapier.com/, -> make app

Same instructions as above, except youtube.

Select webhook in step 2
