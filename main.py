#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import requests
from requests_oauthlib import OAuth1
import json
import codecs
import tkinter as tk
import  tkinter.messagebox
import sys
import smtplib
from email.message import EmailMessage
import winsound
import threading

def emailTo(tweetSrc, ScreenName, timeAt):

    gmailUserName = '@gmail.com'
    gmailPassword = ''
    targetEmail = '.com'

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



class gui(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.createWidgets()

        api_key = ""
        api_secret = ""
        access_token = ""
        access_secret = ""
        self.AUTH = OAuth1(api_key, api_secret, access_token, access_secret)

    def findTwitterThread(self):
        threEvent = threading.Event()
        threEvent.set()
        self.button1['state'] = tk.DISABLED
        thre = threading.Thread(target=self.method)
        thre.start()


    def callEnd(self):
        if tk.messagebox.askyesno('Question?', 'Are you sure you want to quit the program?'):
            root.destroy()
            exit(0)

    def createWidgets(self):
        self.button2 = tk.Button(text='Quit', command=self.callEnd, pady=5, padx=20).pack(side=tk.BOTTOM, fill=tk.X)
        self.button1 = tk.Button()
        self.button1['text'] = 'Start'
        self.button1['command'] = self.findTwitterThread
        self.button1['padx'] = 20
        self.button1['pady'] = 5
        self.button1.pack(side=tk.BOTTOM, fill=tk.X)
        self.textBox = tk.Text()
        self.textBox['wrap'] = tk.WORD
       # self.textBox['font'] = self.helv14
        self.textBox.pack(side=tk.BOTTOM, fill=tk.X)

    def getUserId(scName):
        countN = '&count=1'
        urlIdGet = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=' + scName + countN
        userIdRes = requests.get(urlIdGet, auth=self.AUTH)
        userIdJson = json.loads(userIdRes.text)
        for searchRes in userIdJson:
            scNameID = searchRes['user']['id']
            print(scName + ' ID is : ' + str(scNameID))
            sys.exit('Twitter user ID Search done.')

    def method(self):
        today = datetime.date.today()
        print(today.year, "year", today.month, "month", today.day, "day")
        #getUserId('AbeShinzo') # Input twitter screen name. Example: @realDonaldTrump. Input 'realDonaldTrump'
        self.textBox.insert('1.0','Waiting tweet now...\n\n')


        url = "https://stream.twitter.com/1.1/statuses/filter.json"

        trumpID = 25073877
        civilAirID = 1064031036
        rt_comId = 64643056
        kcnaId = 612926882
        zeroHedge = 18856867

        follewID = [trumpID, civilAirID, rt_comId, kcnaId, zeroHedge]

        searchTypyFollow = 'follow'
        searchTypyTrack = 'track'
        searchWord = u''

        resp = requests.post(url, auth=self.AUTH,  stream=True, data={searchTypyFollow: follewID})

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
                    if userID in follewID:
                        userScName = lineFeed['user']['screen_name']
                        tweetText = lineFeed['text']

                        print(tweetAt)
                        print(userScName)
                        print(tweetText +'\n')
                        contentTweet = codecs.encode(tweetText, 'utf-16')
                        self.textBox.insert('2.0', '\n')
                        self.textBox.insert('3.0', tweetAt + '\n')
                        self.textBox.insert('4.0', userScName + '\n')
                        self.textBox.insert('5.0', tweetText + '\n')

                        try:
                            winsound.Beep(900,1000)  # Beep(frequency, millisecond). The frequency parameter must be in the range 37 through 32767.
                        except RuntimeError:
                            break

                        mailBool = emailTo(tweetText, userScName, tweetAt)
                        if mailBool is False:
                            print('We can not send the E-mail.\n')

                    break

                except(KeyError, TypeError):
                    # print('Key Error')
                    break
root = tk.Tk()
root.geometry('700x500')
root.title('twitter stream GUI')
root['padx'] = 20
root['pady'] = 20
app = gui(master=root)
app.mainloop()

#if __name__ == '__main__':


