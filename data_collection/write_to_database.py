from twitter_api import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET


#import modules
import tweepy
import datetime
import pymysql.cursors


# Only get tweets from this data on
lastDate = datetime.datetime(2018, 10, 12, 16, 13, 41)


# Connect to Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


# Connect to MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"
cusrorType = pymysql.cursors.DictCursor

connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)


#Get 1000 tweets
searchQuery = "@azuresupport"
searched_tweets = []
last_id = -1
max_tweets = 1000

while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=searchQuery, tweet_mode='extended', count=1000, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break


# Create table for raw tweets if there is none
try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()

    # SQL query string
    sqlQuery = "CREATE TABLE IF NOT EXISTS raw_tweets (id_tweet varchar(200), text_tweet text, created_at_status varchar(20), truncated tinyint, retweet_count int, favorite_count int, retweeted tinyint, lang_status varchar(32), id_user varchar(32), id_str_user varchar(32), name_user text, screen_name_user varchar(32), location_user text, description_user text, url_user varchar(100), followers_count_user int, favourites_count_user int, lang_user varchar(32))"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    # Add a row for each tweet
    # Add to filter by last date downloaded "and tweet.created_at > lastDate"
    for tweet in searched_tweets:
        if (tweet.user.screen_name != "azuresupport" and tweet.retweeted == False and tweet.lang == "en" and ('RT @' not in tweet.full_text) and tweet.created_at > lastDate):
            # Assign values to variables
            id_tweet = tweet.id
            text_tweet = tweet.full_text
            created_at_status = tweet.created_at
            truncated = tweet.truncated
            retweet_count = tweet.retweet_count
            favorite_count = tweet.favorite_count
            retweeted = tweet.retweeted
            lang_status = tweet.lang
            # Fields from the user object
            id_user = tweet.user.id
            id_str_user = tweet.user.id_str
            name_user = tweet.user.name
            screen_name_user = tweet.user.screen_name
            location_user = tweet.user.location
            description_user = tweet.user.description
            url_user = tweet.user.url
            followers_count_user = tweet.user.followers_count
            favourites_count_user = tweet.user.favourites_count
            lang_user = tweet.user.lang
            # Insert row
            addrowQuery = 'INSERT INTO raw_tweets (id_tweet, text_tweet, created_at_status, truncated, retweet_count, favorite_count, retweeted, lang_status, id_user, id_str_user, name_user, screen_name_user, location_user, description_user, url_user, followers_count_user, favourites_count_user, lang_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            cursorObject.execute(addrowQuery, (id_tweet, text_tweet, created_at_status, truncated, retweet_count, favorite_count, retweeted, lang_status, id_user, id_str_user, name_user, screen_name_user, location_user, description_user, url_user, followers_count_user, favourites_count_user, lang_user))
            # commit
            connectionObject.commit()

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()
