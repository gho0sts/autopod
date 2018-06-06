"""
Database stuff
"""
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.autopod
articles_collection = db.articles
