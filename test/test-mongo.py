#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from pymongo import MongoClient
from atlasclusterpassword import atlasstring

client = MongoClient(atlasstring)

db = client.azuresupport

print(client.mflix)
