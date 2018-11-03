#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
#import urllib3
import requests
from requests_oauthlib import OAuth1
import json
import codecs
import tkinter
import sys
import smtplib
from email.message import EmailMessage
import winsound

today = datetime.date.today()
print(today.year, "year", today.month, "month", today.day, "day")

api_key = ""
api_secret = ""
access_token = ""
access_secret = ""

AUTH = OAuth1(api_key, api_secret, access_token, access_secret)

url = "https://stream.twitter.com/1.1/statuses/filter.json"

def getUserId(scName):
    countN = '&count=1'
    urlIdGet = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=' + scName + countN
    userIdRes = requests.get(urlIdGet, auth=AUTH)
    userIdJson = json.loads(userIdRes.text)
    for searchRes in userIdJson:
        scNameID = searchRes['user']['id']
        print(scName + ' ID is : '  +  str(scNameID))
        sys.exit('Twitter user ID Search done.')

#getUserId('AbeShinzo') # Input twitter screen name. Example: @realDonaldTrump. Input 'realDonaldTrump'

def emailTo(tweetSrc, ScreenName, timeAt):

    gmailUserName = '@gmail.com'
    gmailPassword = ''
    targetEmail = '@outlook.com'

    message = EmailMessage()
    message.set_content(tweetSrc)
    message['subject'] = ScreenName + ' tweet at ' + timeAt
    message['From'] = gmailUserName
    message['To'] = targetEmail

    smtpServer = smtplib.SMTP('smtp.gmail.com', 587)
    #Connect to smtp.gmail.com on port 465, if you’re using SSL. (Connect on port 587 if you’re using TLS.)
    smtpServer.ehlo()
    smtpServer.starttls()

    try:
        smtpServer.login(gmailUserName, gmailPassword)
    except smtplib.SMTPAuthenticationError:
        print('Sorry, We can not access your google account.Because, this is not secure application for google policy.')
        print('Allow less secure apps at the site of google account, \"Log-in & Security\".')
        print('If it is not, your gmail ID or Password is incorrect.\n')
        return False
    except:
        return False

    smtpServer.send_message(message)
    smtpServer.quit()
    message.clear()
    return True

trumpID = 25073877
civilAirID = 1064031036
rt_comId = 64643056
kcnaId = 612926882

searchTypyFollow = 'follow'
searchTypyTrack = 'track'
searchWord = u''
followUserID = [rt_comId, trumpID, civilAirID, kcnaId]

resp = requests.post(url, auth=AUTH,  stream=True, data={searchTypyFollow: followUserID})

for lineFeed in resp.iter_lines():

    decoded_line = lineFeed.decode('utf-8')
    while True:
        try:
            lineFeed = json.loads(decoded_line)
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
               print(userScName + ': '+ tweetText + '\n')

               try:
                   winsound.Beep(900, 1000) # Beep(frequency, millisecond). The frequency parameter must be in the range 37 through 32767.
               except RuntimeError:
                   break

               emailTo(tweetText, userScName, tweetAt)

           break

        except(KeyError, TypeError):
            #print('Key Error')
            break
