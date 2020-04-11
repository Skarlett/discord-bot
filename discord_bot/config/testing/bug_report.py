from .core import PREFIX

MenuPreamble = "Select the type by using the emojis below"

#####
# Drop report in to these channels
Preamble = f"You may cancel out anytime by using {PREFIX}discard" \
           f" or restart this session with {PREFIX}restart"
DefaultEnding = "Thank you for your report and time. Sincerely, CD Staff."

ReportTo = 665033160098185237

bug_menu = {
  '☣️': ('glitch', (
    'g question 1',
    'g question 2',
    'g question 3',
  )),
  
  '⚙️': ('gamecrash', (
    'c question 1',
    'c question 2',
    'c question 3',
  ))
}
