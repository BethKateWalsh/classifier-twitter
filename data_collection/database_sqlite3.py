import sqlite3

conn = sqlite3.connect('all_tweets.db')
c = conn.cursor()

def create_table() :
    c.execute('CREATE TABLE IF NOT EXISTS raw_tweets(id_user TEXT PRIMARY KEY, id_str_user TEXT, name_user TEXT, screen_name_user TEXT, location_user TEXT, description_user TEXT, url_user TEXT, followers_count_user_user TEXT, favourites_count_user TEXT, lang_user TEXT, id_status TEXT, id_str_status TEXT, text_status TEXT, created_at_statusr TEXT, truncated TEXT, in_reply_to_screen_name TEXT, retweet_count TEXT, favorite_count TEXT, retweeted TEXT, lang_status TEXT)')
    conn.commit()
    c.close()
    conn.close()
# def data_entry() :
# c.execute(INSERT INTO raw_tweets VALUES

create_table()
data_entry()
