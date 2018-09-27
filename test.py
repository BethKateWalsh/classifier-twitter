import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
import numpy as np


# Get tweets from MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"


engine = sqlalchemy.create_engine('mysql+pymysql://root:woodycool123@localhost:3306/azure_support_tweets')
df = pd.read_sql_table("preprocessed_tweets", engine)
data = pd.DataFrame(df)


# Display numbers of each category
# fig = plt.figure(figsize=(8,6))
# df.groupby('main_category').text_tweet.count().plot.bar()
# plt.show()


# Create dictionary of VALUES
labels_data = {'01':'praise','012':'promise','015':'dispraise','12':'helpfulness','13':'feature information','24':'shortcoming','25':'bug report','26':'feature request','211':'content request','214':'improvement request','37':'other app','38':'recommendation','310':'dissuasion','313':'question','316':'other feedback','317':'howto','49':'noise'}
list_of_labels = []
# Add the key it matches in the dictionary
for index, row in data.iterrows():
    # list_of_labels.append
    c = str(row["main_category"])
    list_of_labels.append(labels_data[c])
labels_df = pd.DataFrame(list_of_labels,columns=['label'])
data.insert(3, "label", list_of_labels)


# Text in Numerical Features :)
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(df.text_tweet).toarray()
labels = df.main_category
