import pymysql.cursors
from textblob.classifiers import NaiveBayesClassifier
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Connect to MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"
cusrorType = pymysql.cursors.DictCursor

connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)


# Get tweets from raw_tweets and process
try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()

    # Create new table for processed tweets IF DOSE NOT ALREADY EXSIST
    sqlQuery = "CREATE TABLE IF NOT EXISTS processed_tweets(id_tweet varchar(200), text_tweet text)"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    # Select id_tweet
    cursorObject.execute("SELECT id_tweet, text_tweet FROM raw_tweets")
    for i in cursorObject.fetchall():
        id_tweet = i["id_tweet"];
        text_tweet = i["text_tweet"];

        # Remove mentions, hashtags and special characters :)
        # text_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)"," ",text_tweet).split(" "))

        # Case folding
        text_tweet = text_tweet.casefold()

        # Tokenizer

        # Normalisation

        # Stem words

        # Train classifiers

        # Add tweet text and id to table
        addrowQuery = 'INSERT INTO processed_tweets (id_tweet, text_tweet) VALUES (%s, %s);'
        cursorObject.execute(addrowQuery, (id_tweet, text_tweet))
        connectionObject.commit()

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()
