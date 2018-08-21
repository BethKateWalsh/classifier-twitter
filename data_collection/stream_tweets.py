#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from twitter_api import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET


#import modules
from pymongo import MongoClient
import json
import tweepy

# Connect to Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


#Get 1000 tweets
searchQuery = "@azuresupport"
searched_tweets = []
last_id = -1
max_tweets = 1000

while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=searchQuery, count=100, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

# for tweet in searched_tweets:
# print(tweet.text.encode('utf-8'))

#Write to a json file
path = './'
filename = 'tweet_21_08_2018.json'

tweet_string = '''
{
	"tweet": [{
		"user": "user",
		"id": "id",
		"id_str": "id_str",
		"created_at": "date",
		"coordinates": "coordinates",
		"place": "place",
		"truncated": true,
		"in_reply_to_status_id_str": "in_reply_to_status_id_str",
		"in_reply_to_user_id": "in_reply_to_user_id",
		"in_reply_to_screen_name": "in_reply_to_screen_name",
		"is_quote_status": "is_quote_status",
		"reply_count": "reply_count",
		"retweet_count": "retweet_count",
		"lang": "lang",
		"entities": {
			"hashtags": [],
			"urls": [],
			"user_mentions": [],
			"media": [],
			"symbols": [],
			"polls": []
		},
		"text": "text"
	}]
}
'''
data = json.loads(tweet_string)
new_string = json.dumps(data, indent = 2, sort_keys=True)
print(new_string)


# Connect to database MongoDB



# Import tweets as json files to DB
