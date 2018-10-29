import pandas as pd
import numpy as np
import pymysql.cursors
import sqlalchemy
import datetime
import sys
import re
from wordcloud import WordCloud, STOPWORDS
import preprocessor as p
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt, mpld3
import matplotlib.dates as mdates
import matplotlib.dates as dates
import collections
import contractions
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

username = "amazonhelp"
new_db_name = username + "_predicted_tweets"

# Get tweets from MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"

engine = sqlalchemy.create_engine('mysql+pymysql://root:woodycool123@localhost:3306/azure_support_tweets')
df = pd.read_sql_table(new_db_name, engine)
data = pd.DataFrame(df)

multinomialnb_count = data['multinomialnb_label'].value_counts()
my_plot = multinomialnb_count.plot(kind='bar',legend=None)
my_plot.set_xlabel("Category")
my_plot.set_ylabel("Frequency")

fig = my_plot.get_figure()
fig.savefig('/Users/bethwalsh/Documents/classifier-twitter/app/images/frequency_categories.png')

# No floats
pd.options.display.float_format = '{:,.0f}'.format

# Get dataset ready for multinomialnb_label
frequency_over_time = data[['created_at_status','multinomialnb_label']]
frequency_over_time = frequency_over_time.rename(columns={'created_at_status': 'date'})
frequency_over_time = frequency_over_time.copy()
frequency_over_time['date'] = pd.to_datetime(frequency_over_time['date'],format='%Y-%m-%d %H:%M:%S').apply(lambda x: x.date())

# Multinominal Frequency
bug_report = (frequency_over_time.loc[frequency_over_time['multinomialnb_label'] == "bug report"]).groupby('date').count()
bug_report = bug_report.rename(columns={'multinomialnb_label': 'bug_report'})
question = (frequency_over_time.loc[frequency_over_time['multinomialnb_label'] == "question"]).groupby('date').count()
question = question.rename(columns={'multinomialnb_label': 'question'})
praise = (frequency_over_time.loc[frequency_over_time['multinomialnb_label'] == "praise"]).groupby('date').count()
praise = praise.rename(columns={'multinomialnb_label': 'praise'})
other_feedback = (frequency_over_time.loc[frequency_over_time['multinomialnb_label'] == "other feedback"]).groupby('date').count()
other_feedback = other_feedback.rename(columns={'multinomialnb_label': 'other_feedback'})

# Merge them together
merged_multinomial = bug_report.join(question, lsuffix='bug_report', rsuffix='question')
merged_multinomial = merged_multinomial.join(praise, rsuffix='praise')
merged_multinomial = merged_multinomial.join(other_feedback, rsuffix='other_feedback')
merged_multinomial = merged_multinomial.fillna(0)

merged_multinomial.plot(x_compat=True, legend=None)
locator = dates.DayLocator(
locator.MAXTICKS = 1000
plt.gca().xaxis.set_major_locator(locator)
#plt.gca().xaxis.set_major_locator(dates.DayLocator())
plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%d\n\n%a'))
plt.gcf().autofmt_xdate(rotation=90, ha="left")
plt.savefig('/Users/bethwalsh/Documents/classifier-twitter/app/images/frequency_categories_day.png')

# Python word cloud
# Get all bug report tweets
bug_report_df = data[['created_at_status','multinomialnb_label', 'text_tweet']]
bug_report_df = bug_report_df.loc[bug_report_df['multinomialnb_label'] == "bug report"]

# List of all tweets
list_of_tweets = bug_report_df['text_tweet'].tolist()
bag_of_words = ""
for tweet in list_of_tweets:
    bag_of_words += tweet

# Clean them up
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.RESERVED, p.OPT.SMILEY, p.OPT.NUMBER, p.OPT.HASHTAG)
bag_of_words = p.clean(bag_of_words)
bag_of_words = bag_of_words.casefold()
bag_of_words = contractions.fix(bag_of_words)
bag_of_words = bag_of_words.replace("#", "")
bag_of_words = re.sub(r'([^\s\w]|_)+', ' ', bag_of_words)
bag_of_words = word_tokenize(bag_of_words)
bag_of_words = [word for word in bag_of_words if word not in stopwords.words('english')]
stopwords_others = ['azure', 'thanks', 'hi', 'hello', 'please', 'help']
bag_of_words = [word for word in bag_of_words if word not in stopwords_others]

# Lemmatize words
lemmatizer = WordNetLemmatizer()
bag_of_words_new = []
for w in bag_of_words:
    bag_of_words_new.append(lemmatizer.lemmatize(w))
bag_of_words = bag_of_words_new

# Bigram frequencies
finder = BigramCollocationFinder.from_words(bag_of_words)
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder.apply_freq_filter(3)
scored = finder.score_ngrams(bigram_measures.raw_freq)
scoredList = sorted(scored, reverse=True)
word_dict = {}
listLen = len(scoredList)

# Get the bigram and make a contiguous string for the dictionary key.
# Set the key to the scored value.
for i in range(listLen):
    word_dict['_'.join(scoredList[i][0])] = scoredList[i][1]

# Join together
bag_of_words = " ".join(bag_of_words)
# Get popular bigrams

# Generate word cloud
wordcloud = WordCloud(max_words=200, height=2000, width=4000, background_color="white", collocations=True)
wordcloud.generate_from_frequencies(word_dict)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('/Users/bethwalsh/Documents/classifier-twitter/app/images/bug_report_wordcloud.png')

# Python word cloud
# Get all bug report tweets
question_df = data[['created_at_status','multinomialnb_label', 'text_tweet']]
question_df = question_df.loc[question_df['multinomialnb_label'] == "question"]

# List of all tweets
list_of_tweets = question_df['text_tweet'].tolist()
bag_of_words = ""
for tweet in list_of_tweets:
    bag_of_words += tweet

# Clean them up
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.RESERVED, p.OPT.SMILEY, p.OPT.NUMBER, p.OPT.HASHTAG)
bag_of_words = p.clean(bag_of_words)
bag_of_words = bag_of_words.casefold()
bag_of_words = contractions.fix(bag_of_words)
bag_of_words = bag_of_words.replace("#", "")
bag_of_words = re.sub(r'([^\s\w]|_)+', ' ', bag_of_words)
bag_of_words = word_tokenize(bag_of_words)
bag_of_words = [word for word in bag_of_words if word not in stopwords.words('english')]
stopwords_others = ['azure', 'thanks', 'hi', 'hello', 'please', 'help', 'trying', 'would', 'like']
bag_of_words = [word for word in bag_of_words if word not in stopwords_others]

# Lemmatize words
lemmatizer = WordNetLemmatizer()
bag_of_words_new = []
for w in bag_of_words:
    bag_of_words_new.append(lemmatizer.lemmatize(w))
bag_of_words = bag_of_words_new

# Bigram frequencies
finder = BigramCollocationFinder.from_words(bag_of_words)
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder.apply_freq_filter(3)
scored = finder.score_ngrams(bigram_measures.raw_freq)
scoredList = sorted(scored, reverse=True)
word_dict = {}
listLen = len(scoredList)

# Get the bigram and make a contiguous string for the dictionary key.
# Set the key to the scored value.
for i in range(listLen):
    word_dict['_'.join(scoredList[i][0])] = scoredList[i][1]

# Join together
bag_of_words = " ".join(bag_of_words)

# Generate word cloud
wordcloud = WordCloud(max_words=200, height=2000, width=4000, background_color="white", collocations=True)
wordcloud.generate_from_frequencies(word_dict)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('/Users/bethwalsh/Documents/classifier-twitter/app/images/question_wordcloud.png')

daterange = "Date Range: " + (frequency_over_time.iloc[-1]['date']).strftime("%B %d, %Y") + " - " + (frequency_over_time.iloc[0]['date']).strftime("%B %d, %Y")
