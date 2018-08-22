#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import csv

#Write to a json file
path = './'
filename = 'tweet_21_08_2018.csv'

with open(filename, 'w', newline='') as f:
    thewriterobject = csv.writer(f)

    thewriterobject.writerow(['id_user', 'id_str_user', 'name_user', 'screen_name_user', 'description_user', 'url_user', 'followers_count_user_user', 'favourites_count_user', 'lang_user', 'id_status', 'id_str_status', 'textstatus', 'created_at_status', 'truncated', 'in_reply_to_screen_name', 'retweet_count', 'favorite_count', 'retweeted', 'lang_status'])
