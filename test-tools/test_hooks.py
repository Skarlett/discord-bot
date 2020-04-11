import requests
import time

data = {
  'key': 'BHMm7EpRNXEJQTH1mf7rOADy+wL2OmHUWWbd2LqIbPM=',
  'url': 'https:///asdasd.com/',
  'title': 'asdsd',
  'text': 'tweettweet'
}


for x in ['yt', 'twitter']:
      try:
        requests.post('http://127.0.0.1:8888/'+x, data)
        time.sleep(1)
      except:
          pass
