#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import urllib3
import requests
from requests_oauthlib import OAuth1
import json
import codecs
import tkinter
import sys


today = datetime.date.today()

print(today.year, "year", today.month, "month", today.day, "day")

api_key = ""
api_secret = ""
access_token = ""
access_secret = ""

AUTH = OAuth1(api_key, api_secret, access_token, access_secret)

url = "https://stream.twitter.com/1.1/statuses/filter.json"


followersIdGet = 'https://api.twitter.com/1.1/followers/ids.json?screen_name='

def getUserId():
    scName = "KCNAWatch"
    countN = '&count=1'
    urlIdGet = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=' + scName + countN
    userIdRes = requests.get(urlIdGet, auth=AUTH)
    userIdJson = json.loads(userIdRes.text)
    for searchRes in userIdJson:
        print(searchRes['user']['id'])

#getUserId()

trumpID = 25073877
civilAirID = 1064031036
rt_comId = 64643056
kcnaId = 612926882

searchTypy = u'follow'
searchWord = ''
followUserID = [rt_comId, trumpID, civilAirID, kcnaId]

resp = requests.post(url, auth=AUTH,  stream=True, data={searchTypy: followUserID})

for lineFeed in resp.iter_lines():

    while True:
        try:
            lineFeed = json.loads(lineFeed)
        except ValueError:
            #print('Value Error')
            break

        try:
           userID = lineFeed['user']['id']
           tweetAt = lineFeed['created_at']

           if userID in followUserID:
               userScName = lineFeed['user']['screen_name']
               tweetText = lineFeed['text']
               print(tweetAt)
               print(userScName + '   '+ tweetText + '\n')
               #print(userID)
           break

        except KeyError:
            print('Key Error')
            break
        except TypeError:
            print('Type Error')
            break


