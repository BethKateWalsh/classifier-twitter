import pymysql.cursors

dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"
cusrorType = pymysql.cursors.DictCursor

connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)

try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()

    # SQL query string
    sqlQuery = "CREATE TABLE IF NOT EXISTS raw_tweets(id_tweet int, id_str_status varchar(32), text_status varchar(200), created_at_status varchar(32), truncated varchar(32), in_reply_to_screen_name varchar(32), retweet_count varchar(32), favorite_count varchar(32), retweeted varchar(32), lang_status varchar(32), id_user varchar(32), id_str_user varchar(32), name_user varchar(32), screen_name varchar(32), location_user varchar(32), description_user varchar(32), url_user varchar(32), followers_count_user_user varchar(32), favourites_count_user varchar(32), lang_user varchar(32))"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    # SQL query string
    sqlQuery = "show tables"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    # Fetch all the rows
    rows = cursorObject.fetchall()
    for row in rows:
        print(row)

    # Insert row
    # addrowQuery = "INSERT INTO raw_tweets (id_tweet, id_user, screen_name, DepartmentCode) VALUES (003, 'me', 'beth', 10);"
    # cursorObject.execute(addrowQuery)
    # print("Row inserted")

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()
