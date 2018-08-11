#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from pymongo import MongoClient
from atlasclusterpassword import atlasstring
# connect to MongoDB, change the << MONGODB URL >> to reflect your
# own connection string
mongostring = atlasstring

client = MongoClient(mongostring)
