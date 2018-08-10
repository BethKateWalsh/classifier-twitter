#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import tweepy
from twitter_api import ACCESS_TOKEN
from twitter_api import ACCESS_SECRET
from twitter_api import CONSUMER_KEY
from twitter_api import CONSUMER_SECRET


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# This what will stream the tweets from the Twiiter API.


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted_status:
            return
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["@AzureSupport"])
