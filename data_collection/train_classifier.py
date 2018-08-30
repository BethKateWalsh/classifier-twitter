import nltk
import random
import pymysql
from nltk.tokenize import word_tokenize
from sklearn import naive_baye

# main_category codes
# rating = 0
# user experience = 1
# requirement = 2
# community = 3


# Lists :-)
train_data = []
test_data = []


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
    for i in cursorObject.fetchall()[:20]:

        # Create a tuple list from tweets and categories
        tuple = (i["text_tweet"], i["main_category"])
        train_data.append(tuple)

    for i in cursorObject.fetchall()[20:]:

        # Create a tuple list from tweets and categories
        tuple = (i["text_tweet"])
        test_data.append(tuple)

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()

# Setup classifier
clfrnb = naive_bayes.MultinomialNB()
clfrnb.fit(train_data, train_labels)
predicted_labels = clfrNB.predict(test_data)

for i in predicted_labels:
    print(i)
