import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
import numpy as np
from io import StringIO
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from sklearn import metrics


# Get tweets from MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"

engine = sqlalchemy.create_engine('mysql+pymysql://root:woodycool123@localhost:3306/azure_support_tweets')
df = pd.read_sql_table("preprocessed_tweets", engine)
data = pd.DataFrame(df)

labels_data = {'01':'praise','012':'promise','015':'dispraise','12':'helpfulness','13':'feature information','24':'shortcoming','25':'bug report','26':'feature request','211':'content request','214':'improvement request','37':'other app','38':'recommendation','310':'dissuasion','313':'question','316':'other feedback','317':'howto','49':'noise'}
list_of_labels = []
# Add the key it matches in the dictionary
for index, row in data.iterrows():
    c = str(row["main_category"])
    list_of_labels.append(labels_data[c])
labels_df = pd.DataFrame(list_of_labels,columns=['label'])
data.insert(3, "label", list_of_labels)

col = ['label', 'text_tweet']
data = data[col]
data = data[pd.notnull(df['text_tweet'])]
data.columns = ['label', 'text_tweet']
data['main_category'] = data['label'].factorize()[0]
category_id_df = data[['label', 'main_category']].drop_duplicates().sort_values('main_category')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['main_category', 'label']].values)

# Display numbers of each category
# fig = plt.figure(figsize=(8,6))
# data.groupby('label').text_tweet.count().plot.bar()
# plt.show()


# Text in Numerical Features :)
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(data.text_tweet).toarray()
labels = data.main_category


# Display top features
# N = 2 # for label, main_category in sorted(category_to_id.items()):
#  features_chi2 = chi2(features, labels == main_category)
#  indices = np.argsort(features_chi2[0])
#  feature_names = np.array(tfidf.get_feature_names())[indices]
#  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
#  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
#  print("# '{}':".format(label))
#  print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
#  print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))


X_train, X_test, y_train, y_test = train_test_split(data['text_tweet'], data['label'], random_state = 0, test_size=0.25)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = BernoulliNB().fit(X_train_tfidf, y_train)
pred = clf.predict(count_vect.transform(X_test))
print(accuracy_score(y_test, pred))
# print(metrics.classification_report(pred, y_test))
# print(metrics.confusion_matrix(y_test, pred))
# print(clf.predict(count_vect.transform(["@azuresupport - I hope you all had a tall frosty one once this was fixed.  Yesterday could not have been a good day."])))
