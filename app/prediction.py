from twitter_api import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

#import modules
import tweepy
import datetime
import pymysql.cursors
import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from io import StringIO


def make_prediction(username):

    username = username
    new_db_name = username + "_predicted_tweets"

    # Create CountVectorizer
    count_vect = CountVectorizer()

    # Connect to Twitter API
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Read training set
    df = pd.read_csv("/Users/bethwalsh/Documents/classifier-twitter/training_data.csv")
    data = pd.DataFrame(df)
    # Get modal
    clfMulti = pickle.load(open('multinomialnb_model','rb'))
    # Prepare trainign data for fitting
    X_train, X_test, y_train, y_test = train_test_split(data['text_tweet'], data['main_category'], random_state = 0, test_size=0.25)
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    X_train_counts = count_vect.fit_transform(X_train)
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clfMulti = clfMulti.fit(X_train_tfidf, y_train)

    # Connect to MYSQL database
    dbServerName = "localhost"
    dbUser = "root"
    dbPassword = "woodycool123"
    dbName = "azure_support_tweets"
    cusrorType = pymysql.cursors.DictCursor
    connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)

    # Get 1000 tweets paarmeters
    searchQuery = "@" + username
    searched_tweets = []
    last_id = -1
    max_tweets = 1000

    labels_data = {'01':'praise','012':'promise','015':'dispraise','12':'helpfulness','13':'feature information','24':'shortcoming','25':'bug report','26':'feature request','211':'content request','214':'improvement request','37':'other app','38':'recommendation','310':'dissuasion','313':'question','316':'other feedback','317':'howto','49':'noise'}
    def switch_demo(argument):
        if argument == 1:
            argument = "0" + str(argument);
        return labels_data[str(argument)]

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
    try:
        # Create a cursor object
        cursorObject = connectionObject.cursor()
        sqlQuery = "CREATE TABLE IF NOT EXISTS " + new_db_name +"(id_tweet varchar(200) PRIMARY KEY, text_tweet text, created_at_status varchar(20), truncated tinyint, id_user varchar(32), id_str_user varchar(32), name_user text, screen_name_user varchar(32), location_user text, description_user text, url_user varchar(100), followers_count_user int, favourites_count_user int, lang_user varchar(32), multinomialnb_label varchar(32))"
        cursorObject.execute(sqlQuery)

        # Add a row for each tweet
        # Add to filter by last date downloaded "and tweet.created_at > lastDate"
        for tweet in searched_tweets:
            if (tweet.user.screen_name != username and tweet.retweeted == False and tweet.lang == "en" and ('RT @' not in tweet.full_text)):
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

                # Make prediction
                tweet = text_tweet
                multinomialnb_label = clfMulti.predict(count_vect.transform([tweet]))[0]
                multinomialnb_label = switch_demo(multinomialnb_label)

                Addrowquery = 'INSERT IGNORE INTO ' + new_db_name +'(id_tweet, text_tweet, created_at_status, truncated, id_user, id_str_user, name_user, screen_name_user, location_user, description_user, url_user, followers_count_user, favourites_count_user, lang_user, multinomialnb_label) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
                cursorObject.execute(Addrowquery, (id_tweet, text_tweet, created_at_status, truncated, id_user, id_str_user, name_user, screen_name_user, location_user, description_user, url_user, followers_count_user, favourites_count_user, lang_user, multinomialnb_label))
                # commit
                connectionObject.commit()

    except Exception as e:
        print("Exeception occured:{}".format(e))

    finally:
        connectionObject.close()
