import sqlalchemy
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go


# Get tweets from MYSQL database
dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"

engine = sqlalchemy.create_engine('mysql+pymysql://root:woodycool123@localhost:3306/azure_support_tweets')
df = pd.read_sql_table("predicted_tweets", engine)
data = pd.DataFrame(df)

data = [go.Bar(x=['giraffes', 'orangutans', 'monkeys'], y=[20, 14, 23])]

py.iplot(data, filename='basic-bar')
