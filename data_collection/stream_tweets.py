#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import tweepy

description = ""
loc = ""
text = ""
coords = ""
name = ""
user_created = ""
followers = ""
id_str = ""
created = ""
retweets = ""
bg_color = ""

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '1018566903105839105-cJQsXyqhTLqqf5ES0HbAxR6tD1xoQn'
ACCESS_SECRET = 'zWyBV95tJdxkxNpkCI3xnWA9jJczTYTOiXTazziLzsiYw'
CONSUMER_KEY = 'qP20NzzzTHDumLHWfSTFSXYhT'
CONSUMER_SECRET = 'MDMO0nWhc9NgbyemVLl6bMM2NWyV4qfcO8yWLzKxn13DQUtpOI'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# This what will stream the tweets from the Twiiter API.


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted_status:
            return
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        print(description)

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["@AzureSupport"])
