import pymysql.cursors
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import preprocessor as p
import re
import contractions
from spellchecker import SpellChecker

# Word to not stem
not_stem_words = ['aws', 'amazon', 'dockerhub', 'googlechrome', 'tradelize', 'xbox', 'vsts', 'docker', 'lucidchart', 'facebook', 'bing', 'cloudflare', 'argo', 'safari', 'office365', 'twitter', 'mysql', 'github', 'nodejs', 'ping', 'arm', 'git', 'signalr']
remove_words = ['azure', 'azuresupport']

# Connect to MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"
cusrorType = pymysql.cursors.DictCursor
connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)


# NLTK objects created
porter = PorterStemmer()
wnl = WordNetLemmatizer()

misspelled = []

# Get tweets from raw_tweets and process
try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()

    # Create new table for processed tweets IF DOSE NOT ALREADY EXSIST
    sqlQuery = "CREATE TABLE IF NOT EXISTS preprocessed_tweets(id_tweet varchar(200), text_tweet text, main_category varchar(20))"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    # Select id_tweet
    cursorObject.execute("SELECT id_tweet, text_tweet, main_category FROM raw_tweets")
    for i in cursorObject.fetchall()[:2500]:
        id_tweet = i["id_tweet"];
        text_tweet = i["text_tweet"];
        label_main = i["main_category"];

        # tweet-preprocessor library
        p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.RESERVED, p.OPT.SMILEY, p.OPT.NUMBER)
        text_tweet = p.clean(text_tweet)

        # Case folding
        text_tweet = text_tweet.casefold()

        # Contractions
        text_tweet = contractions.fix(text_tweet)

        # Remove hashtags but keep the words and special characters
        text_tweet = text_tweet.replace("#", "")
        text_tweet = re.sub(r'([^\s\w]|_)+', ' ', text_tweet)

        # Tokenize
        tokenized_tweet = word_tokenize(text_tweet)

        # Correct Spelling
        spell = SpellChecker()
        misspelled = []
        misspelled = spell.unknown(tokenized_tweet)
        for w in misspelled:
            # Replace with correction
            tokenized_tweet = [word.replace(w, spell.correction(w)) for word in tokenized_tweet]

        # Remove the stopwords
        filtered_words = [word for word in tokenized_tweet if word not in stopwords.words('english')]
        tokenized_tweet = filtered_words

        # Stemming (Stop it removing the from words!)
        stemmed_tweet_words = []
        for tweet in tokenized_tweet:
            if tweet in not_stem_words:
                stemmed_tweet_words.append(tweet)
            elif tweet in remove_words:
                pass
            else:
                stemmed_tweet_words.append(porter.stem(tweet))

        # Put string back together
        text_tweet = " ".join(stemmed_tweet_words)

        # Remove multiple spaces
        text_tweet = ' '.join(text_tweet.split())

        # Add tweet text and id to table
        addrowQuery = 'INSERT INTO preprocessed_tweets (id_tweet, text_tweet, main_category) VALUES (%s, %s, %s);'
        cursorObject.execute(addrowQuery, (id_tweet, text_tweet, label_main))
        connectionObject.commit()

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()
