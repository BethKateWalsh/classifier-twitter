import re
import pymysql.cursors

# Connect to MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"
cusrorType = pymysql.cursors.DictCursor
connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)


try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()

    # Create new table for processed tweets IF DOSE NOT ALREADY EXSIST
    sqlQuery = "CREATE TABLE IF NOT EXISTS predicted_tweets(id_tweet varchar(200), text_tweet text, manual_label varchar(20), clf_label varchar(20))"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    # Select id_tweet
    cursorObject.execute("SELECT id_tweet, text_tweet, main_category FROM preprocessed_tweets")
    for i in cursorObject.fetchall()[:2500]:
        id_tweet_add = i["id_tweet"]
        text_tweet_add = i["text_tweet"]
        label_main_add = i["main_category"]
        label_clf_add = clf.predict(count_vect.transform([text_tweet_add]))
        label_clf_add = label_clf_add[0]

        # Add tweet text and id to table
        addrowQuery = 'INSERT INTO predicted_tweets(id_tweet, text_tweet, manual_label, clf_label) VALUES (%s, %s, %s, %s);'
        cursorObject.execute(addrowQuery, (id_tweet_add, text_tweet_add, label_main_add, label_clf_add))
        connectionObject.commit()

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()
