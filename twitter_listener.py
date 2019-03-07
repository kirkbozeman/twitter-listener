"""
Working with streaming Twitter data
2.11.19 - prints to console, can expand to store tweets in MySQL, csv, etc.

"""

import json
import tweepy
import time
from time import sleep

# StreamListener docs: http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
# creation of class is required for stream to work: you are creating a child class of
# the tweepy.StreamListener() parent class and then overriding functions or adding
# functions to complete the functionality
class Listener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            print("Disconnected, waiting 10 seconds. (420 error)")
            sleep(10)
            return False


# get twitter creds
with open('config.json', 'r') as cf:
    config = json.load(cf)
    consumerKey = config["config"]["consumerKey"]
    consumerSecret = config["config"]["consumerSecret"]
    accessToken = config["config"]["accessToken"]
    accessTokenSecret = config["config"]["accessTokenSecret"]

# connect API
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

while True:
    try:
        # create StreamListener and listen for keywords
        mylistener = Listener()
        stream = tweepy.Stream(auth=api.auth, listener=mylistener)
        stream.filter(track=['jawbox', 'fugazi', 'dischord records', 'post-punk'])
    except:
        print("RECONNECT IN 60 SEC")
        time.sleep(60)
        continue

