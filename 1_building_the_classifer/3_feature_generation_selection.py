import sqlalchemy
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn import metrics
import collections, numpy
import pickle


### Connect to MYSQL database
##
#
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"

engine = sqlalchemy.create_engine('mysql+pymysql://root:woodycool123@localhost:3306/azure_support_tweets')
pd.set_option('display.max_colwidth', -1)
df = pd.read_sql_table("preprocessed_tweets", engine)
data = pd.DataFrame(df)


### Training and Test Data Split
##
#
features_train, features_test, labels_train, labels_test = train_test_split(data['text_tweet'], data['main_category'], random_state = 42, test_size=0.25)


### CountVectorizer
##
#
cv = CountVectorizer(ngram_range=(1,2), stop_words='english', min_df=3, max_df=0.50)
features_train_cv = cv.fit_transform(features_train)
# Uncomment to print a matrix count of tokens
# print(features_train_cv.toarray())
print("Feature Count\nCountVectorizer() #", len(cv.get_feature_names()))


### TF-IDF Transformer
##
#
tfidfv = TfidfTransformer(use_idf=True)
features_train_tfidfv = tfidfv.fit_transform(features_train_cv)
print("Feature Set\nTfidfVectorizer() #", features_train_tfidfv.shape)
# Remove to print the top 10 features
# features = tfidfv.get_feature_names()
# feature_order = np.argsort(tfidfv.idf_)[::-1]
# top_n = 10
# top_n_features = [features[i] for i in feature_order[:top_n]]
# print(top_n_features)


### SelectKBest
##
#
selector = SelectKBest(chi2, k=1000)
selector.fit(features_train_tfidfv, labels_train)
features_train_skb = selector.transform(features_train_tfidfv)
#print("Feature Set\nSelectKBest() and chi2 #", selector.shape)


### Train Model
##
#
clf = MultinomialNB()
clf.fit(features_train_skb, labels_train)


### Test Model
##
#
features_test_cv = selector.transform(tfidfv.transform(cv.transform(features_test)))
pred = clf.predict(features_test_cv)


### Get accuracy
##
#
print('Accuracy:', accuracy_score(pred, labels_test))


### Get null accuracy
##
#
print('Null Accuracy:', (labels_test.value_counts().head(1) / len(labels_test)))


### Print a confusion matrix
##
#
print('Confusion Matrix:')
print(metrics.confusion_matrix(labels_test, pred, labels=['25', '313', '01', '49', '316', '26', '211', '015', '24', '37', '317', '13', '214', '012', '12', '310']))
print(collections.Counter(pred))
print(collections.Counter(labels_test))


### Get precision, recall, f1-score
##
#
print('Precision, Recall, F1-Score:')
print(metrics.classification_report(pred, labels_test))


### Save model with pickle
##
#
with open('2_the_application/modal/multinomialnb_modal','wb') as f:
    pickle.dump(clf, f)
