import nltk
import numpy as np
import random
import pymysql
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

corpus = []
labels = []


# Get tweets from MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"
cusrorType = pymysql.cursors.DictCursor
connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)


try:
    cursorObject = connectionObject.cursor()
    cursorObject.execute("SELECT text_tweet, main_category FROM preprocessed_tweets")
    for i in cursorObject.fetchall()[:1500]:

        # Create a numpy array
        sub_corpus = np.array((i["text_tweet"]), (i["main_category"]))
        corpus.append(sub_corpus)

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()


# Split Training and Test Data. First 1500 are labelled
word_vectorizer = CountVectorizer(analyzer='word')
trainset = word_vectorizer.fit_transform(codecs.open(trainfile,'r','utf8'))
tags = [01, 012, 015, 12, 13, 24, 25, 26, 211, 214, 37, 38, 310, 313, 316, 317, 49]
mnb = MultinomialNB()
mnb.fit(trainset, tags)
codecs.open(testfile,'r','utf8')
testset = word_vectorizer.transform(codecs.open(testfile,'r','utf8'))
results = mnb.predict(testset)
print results
