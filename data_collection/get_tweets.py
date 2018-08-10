#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import sys
sys.path.append('C:\Desktop\automated-personas\py')
import tweepy
import datetime
import time

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '1018566903105839105-cJQsXyqhTLqqf5ES0HbAxR6tD1xoQn'
ACCESS_SECRET = 'zWyBV95tJdxkxNpkCI3xnWA9jJczTYTOiXTazziLzsiYw'
CONSUMER_KEY = 'qP20NzzzTHDumLHWfSTFSXYhT'
CONSUMER_SECRET = 'MDMO0nWhc9NgbyemVLl6bMM2NWyV4qfcO8yWLzKxn13DQUtpOI'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


def get_tweets(api, username):
    page = 1
    deadend = False
    while True:
        tweets = api.user_timeline(username, page=page)

        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days < 2:
                print(tweet.text.encode("utf-8"))
            else:
                deadend = True
                return
        if not deadend:
            page+1
            time.sleep(500)


def get_tweets(api, query):
    tweets = api.search(q=query, count=100)
    for tweet in tweets:
        if (datetime.datetime.now() - tweet.created_at).days < 2:
            print(tweet.text.encode("utf-8"))
        else:
            return


get_tweets(api, "@AzureSupport")
