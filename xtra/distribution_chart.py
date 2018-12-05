import sqlalchemy
import pandas as pd
import pymysql.cursors
import matplotlib.pyplot as plt
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from sklearn import metrics


# Get tweets from MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"

engine = sqlalchemy.create_engine('mysql+pymysql://root:woodycool123@localhost:3306/azure_support_tweets')
df = pd.read_sql_table("predicted_tweets", engine)
data = pd.DataFrame(df)

labels_data = {'praise':'01','promise':'012','dispraise':'015','helpfulness':'12','feature information':'13','shortcoming':'24','bug report':'25','26':'feature request','content request':'211','214':'37','improvement request':'38','other app':'310','dissuasion':'310','question':'313','other feedback':'316','howto':'317','noise':'49'}
list_of_labels = []
# Add the key it matches in the dictionary
for index, row in data.iterrows():
    c = str(row["clf_label"])
    list_of_labels.append(c)
labels_df = pd.DataFrame(list_of_labels,columns=['label'])
data.insert(3, "label", list_of_labels)

col = ['label', 'text_tweet']
data = data[col]
data = data[pd.notnull(df['text_tweet'])]
data.columns = ['label', 'text_tweet']
data['clf_label'] = data['label'].factorize()[0]
category_id_df = data[['label', 'clf_label']].drop_duplicates().sort_values('clf_label')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['clf_label', 'label']].values)

# Display numbers of each category
fig = plt.figure(figsize=(8,6))
data.groupby('label').text_tweet.count().plot.bar()
plt.show()
