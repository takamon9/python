import datetime
import urllib3
import requests
from requests_oauthlib import OAuth1
import json
import tkinter

a = 2
b = 3

c = a + b

today = datetime.date.today()
print(c)
print(today.year, "year", today.month, "month", today.day, "day")

api_key = ""
api_secret = ""
access_token = ""
access_secret = ""

auth = OAuth1(api_key, api_secret, access_token, access_secret)

url = "https://stream.twitter.com/1.1/statuses/filter.json"

urlIdGetter = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=KCNAWatch&count=1"
#urlRes = requests.get(urlIdGetter, auth=auth)
#urlRes = json.loads(urlRes.text)
#print(urlRes)

trumpID = 1057728445386539008
civilAirID = 1057797213097725952
rt_comId = 1057870349725982721
kcnaId = 1057871517990744064

r = requests.post(url, auth=auth, stream=True, data={'follow': rt_comId})

for lineFeed in r.iter_lines():

    while True:
        try:
            lineFeed = json.loads(lineFeed)
        except ValueError:
            print('Value Error')
            break

        try:
            answer = lineFeed['text']
            if answer:
                print(answer)
                break
        except KeyError:
            print('Key Error')
            break
        except TypeError:
            print('Type Error')
            break

