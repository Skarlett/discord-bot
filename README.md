# discord-bot
A partially completed discord bot based on the [MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
design pattern allowing for developers to rapidly expand and isolate pieces of the project.
This project was originally written to support a gaming server (for minecraft) that is no longer in use. 

## Operations
+ Server watching
+ Ticket system
+ register user system
+ Announcement systems
+ Bug/hacker report

+ Announce updates from commits on the repository, and from other sources (Youtube, Twitter)
+ Notify users and the administration when game servers are offline


## Operation requirements

### Server watching
Server checking was just attempting to connect to the in-game services to ensure they were online. The bot would do this on a regular interval.
If the server was down, the bot would notify the administration and record the downtime. Once it detected that a service was offline,
it would then edit discord channel names to represent the status of the server.

---

### Ticket system
The ticket system was used to manage the large amount of issues users would report.
It attempted to triage the problem and allocate it appriotately to the correct staff member.

The difference between a ticket, and a report is that a ticket was expected to be replied to, while reports were contained internally by the administration.

#### Implemented
+ create an easy to use menu for users
+ implement timeouts so that users can't flood tickets
+ record the following - who resolved, issued the ticket, when the ticket was resolved, and issued and, if they were raised to senior staff (and by who)
+ manage, and view, and resolve easily for administration (paginate)
+ ticket instances must be stateless to allow for seamless reboots
+ sanatize external data attached to ticket

#### Never implemented
+ Create a special channel/chatroom for ticket resolution.
  Collect the entire conversation, external data,
  and store it offsite with a user acknowledgement notice, also giving the user a copy with the ticket ID

----

### Register User System
The register system was originally invisioned to be a custom white-list system,
where the user would register their discord account with their minecraft account.
This was done by running a command in discord that included the user's in-game name.
The game server would be notified through a plugin, and begin watching for that user's in-game name to send the correct command.
The user would be given a [OTP password](https://en.wikipedia.org/wiki/One-time_password), the user would then send a command in-game with the OTP password,
which would send an http request to the bot confirming the user registered.

It never ended up being a whitelist, but rather got used to determine other people's in-game names.
The administration invisioned it would be later used in give-a-ways.
This was never implemented. 

#### Implemented
+ Record discord user's IDs to a "one-to-many" SQL table using [SQLAlchemy ORM](https://www.sqlalchemy.org/)
+ Timeout if nothing received, and notify user.

#### Never implemented
+ Used as whitelist

---

### Announcement system
The idea of the announcement system was to aggrogate from multiple sources, and notify users when an event occurs. 
This is actually why I added an HTTP Server in the bot, to allow other services to use webhooks we provided.

#### Implemented
+ Integrate [zapier](https://zapier.com/) into the bot for youtube & twitter 
+ Mirror messages from one channel/chatroom into another
+ listen for a bitbucket commit webhook, and send an announcement for an update.
---

### Bug/hacker report
Akin to the ticket system, except one way. It steals many of the features from the tickets to allow easy management.
---




