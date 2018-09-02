import nltk
import numpy as np
import random
import pymysql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split

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
    for i in cursorObject.fetchall()[:30]:

        # Create a tuple list from tweets and categories
        corpus.append(i["text_tweet"])
        labels.append(i["main_category"])

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()

# rating = 0
# user experience = 1
# requirement = 2
# community = 3

# Term Frequency Inverse Document Frequency
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(corpus)
idf = tfidf.idf_
features.shape
# print(dict(zip(tfidf.get_feature_names(), idf)))

# Fit the training set
X_train, X_test, y_train, y_test = train_test_split(corpus, labels, random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)

print(clf.predict(count_vect.transform(["Azure Community Support. I''m trying to find out about something, I''m trying to install office 365 on…"])))
