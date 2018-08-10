#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from pymongo import MongoClient
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your
# own connection string
client = MongoClient(<< MONGODB URL>>)
db = client.admin
# Issue the serverStatus command and print the results
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)
