# Gives ablity to close tickets

###
# until Issue-2462 is resolved, and patched - the backup functionality will be using raw UserIDs
# in
# https://github.com/Rapptz/discord.py/issues/2462
TicketRole = 646042754647982111
SeniorTicketRole = 646043310489731084 # Payment Issues, etc

Seniors = (293122603693113345, 191793436976873473)
Moderators  = ()

TagOnSeniorTickets = True
TagOnNormalTickets = False


TicketChannel = 665032933848907776
TicketAudit = 665033045912322068

OkEmoji = "✅"
Raise = "❓" #"🚫"

DefaultEnding = "Thank you for time, we'll contact you as soon as possible.\nSincerely, CD Team."

PaymentPreamble =\
  "Hey {user}, we're sorry to hear about " \
  "your experience with our payment system. " \
  "We'd like to evaluate your payment as quickly as possible " \
  "by filling out this short questionnaire. Thank you for your patience. " \
  "An Admin will get to you as quickly as possible."

PaymentQuestions = (
  'If you have the receipt of the purchase, ' \
  'please upload a screenshot of it now - add text for any comments. If not please type N/A',
  'Did you recently change your username?',
  'What\'s your current in game name?',
  'What\'s your current email?',
  'Please enter your transaction ID',
  'What was it you bought? (Rank & tier, kit & name, etc)',
  'How long ago did you purchase this?',

)

PruneInterval = 7*24*60*60