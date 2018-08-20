#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from twitter_api import ACCESS_TOKEN
from twitter_api import ACCESS_SECRET
from twitter_api import CONSUMER_KEY
from twitter_api import CONSUMER_SECRET
import pymongo
from pymongo import MongoClient
import json
import tweepy
from pprint import pprint


# Connect to Twitter API

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


# Connect to database MongoDB

client = MongoClient()
db = client.tweet_db
tweet_collection = db.tweet_collection
tweet_collection.create_index([("id", pymongo.ASCENDING)], unique=True)
